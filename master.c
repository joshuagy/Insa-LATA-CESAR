#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h>
 
#define TRUE   1
#define FALSE  0
#define BUFFER_SIZE 1024
#define MAX_CLIENTS 4
#define RESET "\033[0m"
#define RED "\033[31m"
#define CYAN "\033[36m"
#define YELLOW "\033[33m"
#define GREEN "\033[32m"
#define MAGENTA "\033[35m"
#define BLUE    "\033[34m" 

int send_packet(int sockfd, const char *payload, size_t payload_len);
int recv_packet(int sockfd, char **payload, size_t *payload_len);
void add_client(int socket);

int python_socket_fd = -1;
int client_socket[ MAX_CLIENTS + 1 ];
int game_master_socket_fd = -1;

int main(int argc , char *argv[])
{
    if ( argc != 5 ) 
    {
        printf("Usage: %s <IP address> <destination port> <listen port> <mode>\n", argv[0]);
        exit(1);
    }

    int client_fd;

    char * IP_ADDR = argv[1];
    int PORT_EXT = atoi(argv[2]);
    int PORT = atoi(argv[3]);
    int mode = atoi(argv[4]);

    char buffer[ BUFFER_SIZE + 1] = {0};
    char *payload = NULL;
    size_t payload_len;

    int opt = TRUE;
    int master_socket , addrlen , new_socket , activity, i , sd;
	int max_sd;
    struct sockaddr_in address;
    size_t buffer_len; 
    addrlen = sizeof(address);
    
    fd_set readfds;
 
    //initialise all client_socket[] to 0 so not checked
    for (i = 0; i < MAX_CLIENTS; i++) 
    {
        client_socket[i] = 0;
    }
     
    //create a master socket
    if( (master_socket = socket(AF_INET , SOCK_STREAM , 0)) == 0 ) 
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }
 
    //set master socket to allow multiple connections , this is just a good habit, it will work without this
    if( setsockopt(master_socket, SOL_SOCKET, SO_REUSEADDR, (char *)&opt, sizeof(opt)) < 0 )
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
 
    //type of socket created
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );
     
    //bind the socket to localhost port 8888
    if ( bind(master_socket, (struct sockaddr *)&address, sizeof(address)) < 0 ) 
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }
	printf("Listener on port %d \n", PORT);
	
    if ( listen(master_socket, MAX_CLIENTS) < 0 )
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
         
    // Wait for a python client to connect
    printf( YELLOW "Waiting for python client to connect...\n" RESET);
    while (1) 
    {
        if ( (new_socket = accept(master_socket, (struct sockaddr *)&address, (socklen_t *)&addrlen)) < 0 ) 
        {
            perror("accept failed");
            exit(EXIT_FAILURE);
        }

        // check if the client's address matches the desired address
        if ( strcmp(inet_ntoa(address.sin_addr), "127.0.0.1") == 0 ) 
        {
            printf( YELLOW "Python client connected from %s:%d\n" RESET,
                   inet_ntoa(address.sin_addr), ntohs(address.sin_port));
            python_socket_fd = new_socket;
            add_client(python_socket_fd);
            break; // exit the loop and continue with the connected client
        } 
        else 
        {
            printf("Client %s:%d rejected\n", inet_ntoa(address.sin_addr), ntohs(address.sin_port));
            close(new_socket); // close the connection
        }
    }

    // Connect to ip specified by user
    if ( mode == 1 )
    {
        if ( (game_master_socket_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0 ) 
        {
            perror("socket failed");
            exit(EXIT_FAILURE);
        }

        // Set server address and port
        address.sin_family = AF_INET;
        //address.sin_addr.s_addr = INADDR_ANY;
        address.sin_addr.s_addr = inet_addr(IP_ADDR);
        address.sin_port = htons(PORT_EXT);

        // Connect to server
        if ( connect(game_master_socket_fd, (struct sockaddr *)&address, sizeof(address)) < 0 ) 
        {
            perror("connect failed");
            exit(EXIT_FAILURE);
        }

        // Add the client to the list of clients
        add_client(game_master_socket_fd);

        send_packet( python_socket_fd, "PJ", 2 );
    }

	while(TRUE) 
    {
        // clear the socket set
        FD_ZERO(&readfds);
 
        //add master socket to set
        FD_SET(master_socket, &readfds);

        max_sd = master_socket;

        // Add child sockets to set
        for ( i = 0 ; i < MAX_CLIENTS ; i++) 
        {
            //socket descriptor
			sd = client_socket[i];
            
			//if valid socket descriptor then add to read list
			if(sd > 0)
				FD_SET( sd , &readfds);
            
            //highest file descriptor number, need it for the select function
            if(sd > max_sd)
				max_sd = sd;
        }
 
        // Wait for an activity on one of the sockets , timeout is NULL , so wait indefinitely
        activity = select( max_sd + 1 , &readfds , NULL , NULL , NULL);
   
        if ((activity < 0) && (errno!=EINTR)) 
        {
            printf("select error");
        }
         
        // If something happened on the master socket , then its an incoming connection
        if (FD_ISSET(master_socket, &readfds)) 
        {   
            if ( (new_socket = accept(master_socket, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0 )
            {
                perror("accept");
                exit(EXIT_FAILURE);
            }

            printf( YELLOW "New connection , socket fd is %d , ip is : %s , port : %d \n" RESET, new_socket , inet_ntoa(address.sin_addr) , ntohs(address.sin_port));
            if(mode == 0){
                send_packet(python_socket_fd,"NC", sizeof(char)*2);
            }
            add_client(new_socket);
           

            // Alert all clients that a new client has joined
            bzero( buffer, BUFFER_SIZE + 1 );
            sprintf( buffer, "[PROTOCOL][CONNECT]%s:%d", inet_ntoa(address.sin_addr), ntohs(address.sin_port) );
            
            for ( int i = 0; i < MAX_CLIENTS; i++ )
            {
                if ( client_socket[i] != 0 
                        && client_socket[i] != python_socket_fd 
                            && client_socket[i] != new_socket )
                {
                    printf("Sending to %d: %s\n", client_socket[i], buffer );
                    send_packet( client_socket[i], buffer, sizeof(buffer) );
                }
                
            }
        }
        for( i = 0; i < MAX_CLIENTS; i++ ) 
        {
            sd = client_socket[i];
             
            if( FD_ISSET(sd , &readfds) ) 
            {
                if ( recv_packet(sd, &payload, &payload_len) == 0 )
                {
                    // Somebody disconnected , get his details and print
                    getpeername(sd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
                    printf("Host disconnected , ip %s , port %d \n" , inet_ntoa(address.sin_addr) , ntohs(address.sin_port));
                     
                    // Close the socket and mark as 0 in list for reuse
                    close(sd);
                    client_socket[i] = 0;
                    send_packet(python_socket_fd, "PJJ", 3);
                }

                if ( sd == python_socket_fd )
                {
                    printf( CYAN "from python socket (fd: %d): %s [length: %zu]\n" RESET, python_socket_fd, payload, payload_len);
                    for ( int i = 0; i < MAX_CLIENTS; i++ )
                    {
                        if ( client_socket[i] != 0 && client_socket[i] != python_socket_fd )
                        {
                            send_packet(client_socket[i], payload, payload_len);
                        }
                    }
                }
                 else if ( sd == game_master_socket_fd )
                {
                    getpeername(sd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
                    printf( GREEN "from client (fd: %d, ip: %s, port: %d): %s [length: %zu]\n" RESET, sd, inet_ntoa(address.sin_addr), ntohs(address.sin_port), payload, payload_len);
                    
                    if ( strncmp(payload, "[PROTOCOL][CONNECT]", 19) == 0 )
                    {   
                        // get ip to connect to
                        char ip_to_connect[16];
                        int j = 0;
                        for ( int i = 19; i < 35; i++ )
                        {
                            if ( payload[i] == ':' )
                            {
                                ip_to_connect[j] = '\0';
                                break;
                            }
                            ip_to_connect[j] = payload[i];
                            j++;
                        }
                        
                        printf("PROTOCOL MESSAGE CONNECT (try to connect to %s\n", ip_to_connect);

                        // Create client socket
                        if ( (new_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0 ) {
                            perror("socket failed");
                            exit(EXIT_FAILURE);
                        }

                        // Set server address and port
                        address.sin_family = AF_INET;
                        // address.sin_addr.s_addr = inet_addr("192.168.72.202");
                        // address.sin_addr.s_addr = INADDR_ANY;
                        address.sin_addr.s_addr = inet_addr(ip_to_connect);
                        address.sin_port = htons(8888);

                        // Connect to server
                        if ( connect(new_socket, (struct sockaddr *)&address, sizeof(address)) < 0 ) {
                            perror("connect failed");
                            exit(EXIT_FAILURE);
                        }

                        // add client to client list
                        add_client(new_socket);
                    }
                    else
                    {
                        send_packet(python_socket_fd, payload, payload_len);
                    }
                }
                else
                {
                    send_packet(python_socket_fd, payload, payload_len);
                }
            }
        }
    }
     
    return 0;
}

int send_packet(int sockfd, const char *payload, size_t payload_len) 
{
    // Calculate the total length of the packet (payload + header)
    size_t packet_len = payload_len + sizeof(uint32_t);

    // Allocate a buffer for the packet
    char *packet = malloc(packet_len);
    if (!packet) {
        perror("malloc");
        return -1;
    }

    // Write the length field in network byte order
    uint32_t length = htonl(payload_len);
    memcpy(packet, &length, sizeof(length));

    // Copy the payload into the packet buffer
    memcpy(packet + sizeof(length), payload, payload_len);

    // Send the packet
    ssize_t ret = send(sockfd, packet, packet_len, 0);
    if (ret < 0) {
        perror("send");
    }

    // Free the packet buffer
    free(packet);

    return ret;
}

int recv_packet(int sockfd, char **payload, size_t *payload_len) 
{

    // Read the length field from the stream
    uint32_t length;
    ssize_t ret = recv(sockfd, &length, sizeof(length), 0);

    if (ret < 0) {
        perror("recv");
        return -1;
    } else if (ret == 0) {
        // The connection was closed by the peer
        return 0;
    }

    // Convert the length field from network byte order to host byte order
    *payload_len = ntohl(length);
    // printf("next payload length: %d\n", *payload_len);

    // Allocate a buffer for the payload
    *payload = malloc(*payload_len);
    if (!*payload) {
        perror("malloc");
        return -1;
    }

    // Read the payload from the stream
    ret = recv(sockfd, *payload, *payload_len, 0);

    if (ret < 0) {
        perror("recv");
        free(*payload);
        return -1;
    } else if (ret == 0) {
        // The connection was closed by the peer
        free(*payload);
        return 0;
    }
    return ret;
}

//add new socket to array of sockets
void add_client(int socket)
{
    for (int i = 0; i < MAX_CLIENTS; i++) 
    {
        //if position is empty
        if( client_socket[i] == 0 )
        {
            client_socket[i] = socket;
            printf("Adding to list of sockets as %d\n" , i);
            break;
        }
    }
}