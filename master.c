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

int send_packet(int sockfd, const char *payload, size_t payload_len);
int recv_packet(int sockfd, char **payload, size_t *payload_len);

typedef struct client {
    int socket;
    char ip[20];
    int port;
} Client;

Client *clients[ MAX_CLIENTS + 1];

int active_connections = 0;
int python_socket_fd = -1;
int client_socket[ MAX_CLIENTS + 1 ];

void print_all_clients(void) 
{
    for (int i = 0; i < MAX_CLIENTS; i++) {
        if (clients[i] != NULL) {
            printf("Client %d: %s:%d\n", i, clients[i]->ip, clients[i]->port);
        }
    }
}

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

    char *payload = NULL;
    size_t payload_len;

    int opt = TRUE;
    int master_socket , addrlen , new_socket , activity, i , valread , sd;
	int max_sd;
    struct sockaddr_in address;
    size_t buffer_len; 
    char buffer[BUFFER_SIZE + 1];  //data buffer of 1K
     
    //set of socket descriptors
    fd_set readfds;
     
    char *first_message = "Connected to server.\n";
 
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
	
    //try to specify maximum of 3 pending connections for the master socket
    if ( listen(master_socket, 4) < 0 )
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
     
    //accept the incoming connection
    addrlen = sizeof(address);
    
    if ( mode == 1 )
    {
        // Create client socket
        if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
            perror("socket failed");
            exit(EXIT_FAILURE);
        }

        // Set server address and port
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = inet_addr(IP_ADDR);
        // address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(PORT_EXT);

        // Connect to server
        if ( connect(client_fd, (struct sockaddr *)&address, sizeof(address)) < 0 ) {
            perror("connect failed");
            exit(EXIT_FAILURE);
        }
    }

	while(TRUE) 
    {
        // clear buffer 
        bzero(buffer, BUFFER_SIZE + 1);

        // clear the socket set
        FD_ZERO(&readfds);
 
        //add master socket to set
        FD_SET(master_socket, &readfds);

        if ( mode == 1 )
        {
            client_socket[0] = client_fd;
            
            if ( client_fd > max_sd )
            {
                max_sd = client_fd;
            }
        }
        else 
        {
            max_sd = master_socket;
        }
		
        //add child sockets to set
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
 
        //wait for an activity on one of the sockets , timeout is NULL , so wait indefinitely
        activity = select( max_sd + 1 , &readfds , NULL , NULL , NULL);
   
        if ((activity < 0) && (errno!=EINTR)) 
        {
            printf("select error");
        }
         
        //If something happened on the master socket , then its an incoming connection
        if (FD_ISSET(master_socket, &readfds)) 
        {   
            if ((new_socket = accept(master_socket, (struct sockaddr *)&address, (socklen_t*)&addrlen))<0)
            {
                perror("accept");
                exit(EXIT_FAILURE);
            }

            // We assume that the first connection is the python sender
            if ( python_socket_fd == -1 )
            {
                python_socket_fd = new_socket;
                printf("Python sender connected. fd: %d\n", python_socket_fd);
            }

            //inform user of socket number - used in send and receive commands
            printf("New connection , socket fd is %d , ip is : %s , port : %d \n" , new_socket , inet_ntoa(address.sin_addr) , ntohs(address.sin_port));
            
            //add new socket to array of sockets
            for (i = 0; i < MAX_CLIENTS; i++) 
            {
                //if position is empty
				if( client_socket[i] == 0 )
                {
                    client_socket[i] = new_socket;
                    printf("Adding to list of sockets as %d\n" , i);
                    clients[ i ] = (Client *)malloc(sizeof(Client));
                    strcpy(clients[ i ]->ip, inet_ntoa(address.sin_addr));
                    clients[ i ]->port = ntohs(address.sin_port);
                    clients[ i ]->socket = new_socket;
                    active_connections++;
					break;
                }
            }

            print_all_clients();
            // alert all clients that a new client has joined.
            // send_to_clients(client_socket, first_message, python_socket_fd);
        }
        //else its some IO operation on some other socket :)
        for( i = 0; i < MAX_CLIENTS; i++ ) 
        {
            sd = client_socket[i];
             
            if( FD_ISSET(sd , &readfds) ) 
            {
                //Check if it was for closing , and also read the incoming message
                // if ( (valread = recv( sd , buffer, BUFFER_SIZE, 0)) == 0 )
                
                if ( recv_packet(sd, &payload, &payload_len) == 0 )
                {
                    //Somebody disconnected , get his details and print
                    getpeername(sd, (struct sockaddr*)&address, (socklen_t*)&addrlen);
                    printf("Host disconnected , ip %s , port %d \n" , inet_ntoa(address.sin_addr) , ntohs(address.sin_port));
                     
                    //Close the socket and mark as 0 in list for reuse
                    close(sd);
                    client_socket[i] = 0;
                    free(clients[i]);
                    active_connections--;
                }
                
                // buffer[valread] = '\0';

                if ( sd == python_socket_fd )
                {
                    //printf("Message received from python socket (fd: %d): %s [length: %d]\n", python_socket_fd, payload, payload_len);
                    for ( int i = 0; i < active_connections; i++ )
                    {
                        if ( client_socket[i] != python_socket_fd )
                        {
                            send_packet(client_socket[i], payload, payload_len);
                        }
                    }
                }
                // Send to python socket the incoming message
                else
                {
                    // printf("Message received from client (fd: %d): %s\n", sd, payload);
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