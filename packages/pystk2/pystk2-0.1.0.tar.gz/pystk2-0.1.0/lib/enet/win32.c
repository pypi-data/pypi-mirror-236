/** 
 @file  win32.c
 @brief ENet Win32 system specific functions
*/
#ifdef _WIN32

#define ENET_BUILDING_LIB 1
#include "enet/enet.h"
#include <ws2tcpip.h>
#include <windows.h>
#include <mmsystem.h>

static enet_uint32 timeBase = 0;

// Global variable handled by STK
extern int isIPv6Socket(void);

int
enet_initialize (void)
{
    WORD versionRequested = MAKEWORD (1, 1);
    WSADATA wsaData;
   
    if (WSAStartup (versionRequested, & wsaData))
       return -1;

    if (LOBYTE (wsaData.wVersion) != 1||
        HIBYTE (wsaData.wVersion) != 1)
    {
       WSACleanup ();
       
       return -1;
    }

    timeBeginPeriod (1);

    return 0;
}

void
enet_deinitialize (void)
{
    timeEndPeriod (1);

    WSACleanup ();
}

enet_uint32
enet_host_random_seed (void)
{
    return (enet_uint32) timeGetTime ();
}

enet_uint32
enet_time_get (void)
{
    return (enet_uint32) timeGetTime () - timeBase;
}

void
enet_time_set (enet_uint32 newTimeBase)
{
    timeBase = (enet_uint32) timeGetTime () - newTimeBase;
}

int
enet_address_set_host_ip (ENetAddress * address, const char * name)
{
    enet_uint8 vals [4] = { 0, 0, 0, 0 };
    int i;

    for (i = 0; i < 4; ++ i)
    {
        const char * next = name + 1;
        if (* name != '0')
        {
            long val = strtol (name, (char **) & next, 10);
            if (val < 0 || val > 255 || next == name || next - name > 3)
              return -1;
            vals [i] = (enet_uint8) val;
        }

        if (* next != (i < 3 ? '.' : '\0'))
          return -1;
        name = next + 1;
    }

    memcpy (& address -> host.p0, vals, sizeof (enet_uint32));
    return 0;
}

int
enet_address_set_host (ENetAddress * address, const char * name)
{
    struct hostent * hostEntry;

    hostEntry = gethostbyname (name);
    if (hostEntry == NULL ||
        hostEntry -> h_addrtype != AF_INET)
      return enet_address_set_host_ip (address, name);

    address -> host.p0 = * (enet_uint32 *) hostEntry -> h_addr_list [0];

    return 0;
}

int
enet_address_get_host_ip (const ENetAddress * address, char * name, size_t nameLength)
{
    char * addr = inet_ntoa (* (struct in_addr *) & address -> host.p0);
    if (addr == NULL)
        return -1;
    else
    {
        size_t addrLen = strlen(addr);
        if (addrLen >= nameLength)
          return -1;
        memcpy (name, addr, addrLen + 1);
    }
    return 0;
}

int
enet_address_get_host (const ENetAddress * address, char * name, size_t nameLength)
{
    struct in_addr in;
    struct hostent * hostEntry;
 
    in.s_addr = address -> host.p0;
    
    hostEntry = gethostbyaddr ((char *) & in, sizeof (struct in_addr), AF_INET);
    if (hostEntry == NULL)
      return enet_address_get_host_ip (address, name, nameLength);
    else
    {
       size_t hostLen = strlen (hostEntry -> h_name);
       if (hostLen >= nameLength)
         return -1;
       memcpy (name, hostEntry -> h_name, hostLen + 1);
    }

    return 0;
}

int
enet_socket_bind (ENetSocket socket, const ENetAddress * address)
{
    if (isIPv6Socket() == 1)
    {
        struct sockaddr_in6 sin;
        memset (& sin, 0, sizeof (sin));
        sin.sin6_family = AF_INET6;

        if (address != NULL)
        {
            sin.sin6_port = ENET_HOST_TO_NET_16 (address -> port);
            memcpy (sin.sin6_addr.s6_addr, &address->host.p0, 16);
        }
        else
        {
            sin.sin6_port = 0;
            sin.sin6_addr = in6addr_any;
        }

        return bind (socket,
                    (struct sockaddr *) & sin,
                    sizeof (struct sockaddr_in6)) == SOCKET_ERROR ? -1 : 0;
    }
    else
    {
        struct sockaddr_in sin;

        memset (& sin, 0, sizeof (struct sockaddr_in));

        sin.sin_family = AF_INET;

        if (address != NULL)
        {
            sin.sin_port = ENET_HOST_TO_NET_16 (address -> port);
            sin.sin_addr.s_addr = address -> host.p0;
        }
        else
        {
            sin.sin_port = 0;
            sin.sin_addr.s_addr = INADDR_ANY;
        }

        return bind (socket,
                    (struct sockaddr *) & sin,
                    sizeof (struct sockaddr_in)) == SOCKET_ERROR ? -1 : 0;
    }
}

int
enet_socket_get_address (ENetSocket socket, ENetAddress * address)
{
    if (isIPv6Socket() == 1)
    {
        struct sockaddr_in6 sin;
        memset (& sin, 0, sizeof (sin));
        socklen_t sinLength = sizeof (struct sockaddr_in6);

        if (getsockname (socket, (struct sockaddr *) & sin, & sinLength) == -1)
            return -1;

        memcpy (& address->host.p0, sin.sin6_addr.s6_addr, 16);
        address -> host.p4 = sin.sin6_scope_id;
        address -> port = ENET_NET_TO_HOST_16 (sin.sin6_port);

        return 0;
    }
    else
    {
        struct sockaddr_in sin;
        socklen_t sinLength = sizeof (struct sockaddr_in);

        if (getsockname (socket, (struct sockaddr *) & sin, & sinLength) == -1)
            return -1;

        address -> host.p0 = (enet_uint32) sin.sin_addr.s_addr;
        address -> port = ENET_NET_TO_HOST_16 (sin.sin_port);

        return 0;
    }
}

int
enet_socket_listen (ENetSocket socket, int backlog)
{
    return listen (socket, backlog < 0 ? SOMAXCONN : backlog) == SOCKET_ERROR ? -1 : 0;
}

ENetSocket
enet_socket_create (ENetSocketType type)
{
    int pf_family = isIPv6Socket() == 1 ? PF_INET6 : PF_INET;
    SOCKET socket_fd = socket (pf_family, type == ENET_SOCKET_TYPE_DATAGRAM ? SOCK_DGRAM : SOCK_STREAM, 0);
    if (isIPv6Socket() == 1 && socket_fd != INVALID_SOCKET)
    {
        int no = 0;
        // Allow IPv6 socket listen to IPv4 connection (as long as the host has IPv4 address)
        // We always use dual stack in STK
        setsockopt (socket_fd, IPPROTO_IPV6, IPV6_V6ONLY, (void *) & no, sizeof (no));
    }
    return socket_fd;
}

int
enet_socket_set_option (ENetSocket socket, ENetSocketOption option, int value)
{
    int result = SOCKET_ERROR;
    switch (option)
    {
        case ENET_SOCKOPT_NONBLOCK:
        {
            u_long nonBlocking = (u_long) value;
            result = ioctlsocket (socket, FIONBIO, & nonBlocking);
            break;
        }

        case ENET_SOCKOPT_BROADCAST:
            result = setsockopt (socket, SOL_SOCKET, SO_BROADCAST, (char *) & value, sizeof (int));
            break;

        case ENET_SOCKOPT_REUSEADDR:
            result = setsockopt (socket, SOL_SOCKET, SO_REUSEADDR, (char *) & value, sizeof (int));
            break;

        case ENET_SOCKOPT_RCVBUF:
            result = setsockopt (socket, SOL_SOCKET, SO_RCVBUF, (char *) & value, sizeof (int));
            break;

        case ENET_SOCKOPT_SNDBUF:
            result = setsockopt (socket, SOL_SOCKET, SO_SNDBUF, (char *) & value, sizeof (int));
            break;

        case ENET_SOCKOPT_RCVTIMEO:
            result = setsockopt (socket, SOL_SOCKET, SO_RCVTIMEO, (char *) & value, sizeof (int));
            break;

        case ENET_SOCKOPT_SNDTIMEO:
            result = setsockopt (socket, SOL_SOCKET, SO_SNDTIMEO, (char *) & value, sizeof (int));
            break;

        case ENET_SOCKOPT_NODELAY:
            result = setsockopt (socket, IPPROTO_TCP, TCP_NODELAY, (char *) & value, sizeof (int));
            break;

        default:
            break;
    }
    return result == SOCKET_ERROR ? -1 : 0;
}

int
enet_socket_get_option (ENetSocket socket, ENetSocketOption option, int * value)
{
    int result = SOCKET_ERROR, len;
    switch (option)
    {
        case ENET_SOCKOPT_ERROR:
            len = sizeof(int);
            result = getsockopt (socket, SOL_SOCKET, SO_ERROR, (char *) value, & len);
            break;

        default:
            break;
    }
    return result == SOCKET_ERROR ? -1 : 0;
}

int
enet_socket_connect (ENetSocket socket, const ENetAddress * address)
{
    struct sockaddr_in sin;
    int result;

    memset (& sin, 0, sizeof (struct sockaddr_in));

    sin.sin_family = AF_INET;
    sin.sin_port = ENET_HOST_TO_NET_16 (address -> port);
    sin.sin_addr.s_addr = address -> host.p0;

    result = connect (socket, (struct sockaddr *) & sin, sizeof (struct sockaddr_in));
    if (result == SOCKET_ERROR && WSAGetLastError () != WSAEWOULDBLOCK)
      return -1;

    return 0;
}

ENetSocket
enet_socket_accept (ENetSocket socket, ENetAddress * address)
{
    SOCKET result;
    struct sockaddr_in sin;
    int sinLength = sizeof (struct sockaddr_in);

    result = accept (socket, 
                     address != NULL ? (struct sockaddr *) & sin : NULL, 
                     address != NULL ? & sinLength : NULL);

    if (result == INVALID_SOCKET)
      return ENET_SOCKET_NULL;

    if (address != NULL)
    {
        address -> host.p0 = (enet_uint32) sin.sin_addr.s_addr;
        address -> port = ENET_NET_TO_HOST_16 (sin.sin_port);
    }

    return result;
}

int
enet_socket_shutdown (ENetSocket socket, ENetSocketShutdown how)
{
    return shutdown (socket, (int) how) == SOCKET_ERROR ? -1 : 0;
}

void
enet_socket_destroy (ENetSocket socket)
{
    if (socket != INVALID_SOCKET)
      closesocket (socket);
}

int
enet_socket_send (ENetSocket socket,
                  const ENetAddress * address,
                  const ENetBuffer * buffers,
                  size_t bufferCount)
{
    struct sockaddr_storage sin;
    memset (& sin, 0, sizeof (sin));
    size_t sin_size = 0;

    DWORD sentLength;

    if (address != NULL)
    {
        if (isIPv6Socket() == 1)
        {
            struct sockaddr_in6 * v6 = (struct sockaddr_in6 *) & sin;
            v6 -> sin6_family = AF_INET6;
            v6 -> sin6_port = ENET_HOST_TO_NET_16 (address -> port);
            memcpy (v6 -> sin6_addr.s6_addr, & address -> host.p0, 16);
            v6 -> sin6_scope_id = address -> host.p4;

            sin_size = sizeof (struct sockaddr_in6);
        }
        else
        {
            struct sockaddr_in * v4 = (struct sockaddr_in *) & sin;
            v4 -> sin_family = AF_INET;
            v4 -> sin_port = ENET_HOST_TO_NET_16 (address -> port);
            v4 -> sin_addr.s_addr = address -> host.p0;

            sin_size = sizeof (struct sockaddr_in);
        }
    }

    if (WSASendTo (socket, 
                   (LPWSABUF) buffers,
                   (DWORD) bufferCount,
                   & sentLength,
                   0,
                   address != NULL ? (struct sockaddr *) & sin : NULL,
                   address != NULL ? (int)sin_size : 0,
                   NULL,
                   NULL) == SOCKET_ERROR)
    {
       if (WSAGetLastError () == WSAEWOULDBLOCK)
         return 0;

       return -1;
    }

    return (int) sentLength;
}

int
enet_socket_receive (ENetSocket socket,
                     ENetAddress * address,
                     ENetBuffer * buffers,
                     size_t bufferCount)
{
    INT sinLength = sizeof (struct sockaddr_storage);
    DWORD flags = 0,
          recvLength;
    struct sockaddr_storage sin;
    memset (& sin, 0, sizeof (sin));

    if (WSARecvFrom (socket,
                     (LPWSABUF) buffers,
                     (DWORD) bufferCount,
                     & recvLength,
                     & flags,
                     address != NULL ? (struct sockaddr *) & sin : NULL,
                     address != NULL ? & sinLength : NULL,
                     NULL,
                     NULL) == SOCKET_ERROR)
    {
       switch (WSAGetLastError ())
       {
       case WSAEWOULDBLOCK:
       case WSAECONNRESET:
          return 0;
       }

       return -1;
    }

    if (flags & MSG_PARTIAL)
      return -1;

    if (address != NULL)
    {
        switch (sin.ss_family)
        {
        case AF_INET:
            // Should not happen if dual stack is working
            if (isIPv6Socket() == 1)
                return -1;
            struct sockaddr_in * v4 = (struct sockaddr_in *) & sin;
            address -> host.p0 = (enet_uint32) v4 -> sin_addr.s_addr;
            address -> port = ENET_NET_TO_HOST_16 (v4->sin_port);
            break;
        case AF_INET6:
            if (isIPv6Socket() != 1)
            return -1;
            struct sockaddr_in6 * v6 = (struct sockaddr_in6 *) & sin;
            memcpy (& address -> host.p0, v6 -> sin6_addr.s6_addr, 16);
            address -> host.p4 = v6 -> sin6_scope_id;
            address -> port = ENET_NET_TO_HOST_16 (v6 -> sin6_port);
            break;
        default:
            return -1;
        }
    }

    return (int) recvLength;
}

int
enet_socketset_select (ENetSocket maxSocket, ENetSocketSet * readSet, ENetSocketSet * writeSet, enet_uint32 timeout)
{
    struct timeval timeVal;

    timeVal.tv_sec = timeout / 1000;
    timeVal.tv_usec = (timeout % 1000) * 1000;

    return select (maxSocket + 1, readSet, writeSet, NULL, & timeVal);
}

int
enet_socket_wait (ENetSocket socket, enet_uint32 * condition, enet_uint32 timeout)
{
    fd_set readSet, writeSet;
    struct timeval timeVal;
    int selectCount;
    
    timeVal.tv_sec = timeout / 1000;
    timeVal.tv_usec = (timeout % 1000) * 1000;
    
    FD_ZERO (& readSet);
    FD_ZERO (& writeSet);

    if (* condition & ENET_SOCKET_WAIT_SEND)
      FD_SET (socket, & writeSet);

    if (* condition & ENET_SOCKET_WAIT_RECEIVE)
      FD_SET (socket, & readSet);

    selectCount = select (socket + 1, & readSet, & writeSet, NULL, & timeVal);

    if (selectCount < 0)
      return -1;

    * condition = ENET_SOCKET_WAIT_NONE;

    if (selectCount == 0)
      return 0;

    if (FD_ISSET (socket, & writeSet))
      * condition |= ENET_SOCKET_WAIT_SEND;
    
    if (FD_ISSET (socket, & readSet))
      * condition |= ENET_SOCKET_WAIT_RECEIVE;

    return 0;
} 

#endif

