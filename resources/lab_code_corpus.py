"""Actual lab source code from OS lab directories."""

LAB_CODE_SNIPPETS = [

    # ─── LAB 1: Makefile with static and shared libraries ─────────────────
    (r'''test: main.o libmystaticlib.a libmysharedlib.so
	gcc -o test main.o -L. -lmystaticlib -lmysharedlib

main.o: main.c myheader.h
	gcc -c main.c

f1.o: f1.c
	gcc -c f1.c

f2.o: f2.c
	gcc -c -fpic f2.c

libmysharedlib.so: f2.o
	gcc -shared -o libmysharedlib.so f2.o

libmystaticlib.a: f1.o
	ar cr libmystaticlib.a f1.o

clean:
	rm *.o libmystaticlib.a libmysharedlib.so test
''', "Makefile lab1 static library shared library ar gcc fpic linking"),

    # ─── LAB 2+4: twoprocs.c — basic fork parent child ───────────────────
    ('''#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main(void) {
   pid_t childpid;
   int x;

   x = 0;
   printf("I am process %ld and my x is %d\\n", (long)getpid(), x);
   childpid = fork();
   if (childpid == -1) {
      perror("Failed to fork");
      return 1;
   }
   if (childpid == 0)  {                           /* child code */
      x = 5;
      printf("I am child %ld my parent is %ld and my value of x is %d\\n", (long)getpid(), (long)getppid(), x);
      return 0;
   }
   else   {                                       /* parent code */
      x = 10;
      wait(NULL);
      printf("I am parent %ld my parent is %ld and my value of x is %d\\n", (long)getpid(), (long)getppid(), x);
      return 0;
   }
}
''', "C fork two processes parent child wait getpid getppid lab2"),

    # ─── LAB 2+4: simplefan.c ────────────────────────────────────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main (int argc, char *argv[]) {
   pid_t childpid = 0;
   int i, n;

   if (argc != 2){
      fprintf(stderr, "Usage: %s processes\\n", argv[0]);
      return 1;
   }
   n = atoi(argv[1]);
   for (i = 1; i < n; i++)
      if ((childpid = fork()) <= 0)
         break;

   fprintf(stderr, "i:%d  process ID:%ld  parent ID:%ld  child ID:%ld\\n",
           i, (long)getpid(), (long)getppid(), (long)childpid);
   return 0;
}
''', "C fork fan process tree one parent multiple children lab2"),

    # ─── LAB 2+4: simplechain.c ──────────────────────────────────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main (int argc, char *argv[]) {
   pid_t childpid = 0;
   int i, n;

   if (argc != 2){
      fprintf(stderr, "Usage: %s processes\\n", argv[0]);
      return 1;
   }
   n = atoi(argv[1]);
   for (i = 1; i < n; i++)
      if (childpid = fork())   // parent breaks out
         break;

   fprintf(stderr, "i:%d  process ID:%ld  parent ID:%ld  child ID:%ld\\n",
           i, (long)getpid(), (long)getppid(), (long)childpid);
   return 0;
}
''', "C fork chain process tree each child creates next lab2"),

    # ─── LAB 2+4: parentwritepipe.c ──────────────────────────────────────
    ('''#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#define BUFSIZE 10

int main(void) {
   char bufin[BUFSIZE] = "empty";
   char bufout[] = "hello";
   int bytesin;
   pid_t childpid;
   int fd[2];

   if (pipe(fd) == -1) {
      perror("Failed to create the pipe");
      return 1;
   }
   bytesin = strlen(bufin);
   childpid = fork();
   if (childpid == -1) {
      perror("Failed to fork");
      return 1;
   }
   if (childpid)                                       /* parent code */
      write(fd[1], bufout, strlen(bufout)+1);
   else                                                 /* child code */
      bytesin = read(fd[0], bufin, BUFSIZE);
   fprintf(stderr, "[%ld]:my bufin is {%s}, my bufout is {%s}\\n",
           (long)getpid(),  bufin, bufout);
   return 0;
}
''', "C pipe parent write child read fork fd communication lab2"),

    # ─── LAB 2+4: redirect.c — dup2 stdout to file ──────────────────────
    ('''#include <fcntl.h>
#include <stdio.h>
#include <sys/stat.h>
#include <unistd.h>
#define CREATE_FLAGS (O_WRONLY | O_CREAT | O_APPEND)
#define CREATE_MODE (S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH)

int main(void) {
   int fd;
   fd = open("my.file", O_WRONLY );
   if (fd == -1) {
       perror("Failed to open my.file");
       return 1;
   }
   if (dup2(fd, STDOUT_FILENO) == -1) {
      perror("Failed to redirect standard output");
      return 1;
   }
   if (close(fd) == -1) {
      perror("Failed to close the file");
      return 1;
   }
   if (write(STDOUT_FILENO, "OK", 2) == -1) {
      perror("Failed in writing to file");
      return 1;
   }
   return 0;
}
''', "C dup2 redirect stdout to file open write lab2"),

    # ─── LAB 2+4: simpleredirect.c — pipe ls | wc ───────────────────────
    ('''#include <errno.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void) {
   pid_t childpid;
   int fd[2];

   if ((pipe(fd) == -1) || ((childpid = fork()) == -1)) {
      perror("Failed to setup pipeline");
      return 1;
   }

   if (childpid == 0) {                           /* ls is the child */
      if (dup2(fd[1], STDOUT_FILENO) == -1)
         perror("Failed to redirect stdout of ls");
      else if ((close(fd[0]) == -1) || (close(fd[1]) == -1))
         perror("Failed to close extra pipe descriptors on ls");
      else {
         execl("/bin/ls", "ls", "-l", NULL);
         perror("Failed to exec ls");
      }
      return 1;
   }
   if (dup2(fd[0], STDIN_FILENO) == -1)               /* wc is the parent */
       perror("Failed to redirect stdin of sort");
   else if ((close(fd[0]) == -1) || (close(fd[1]) == -1))
       perror("Failed to close extra pipe file descriptors on sort");
   else {
      execl("/bin/wc", "wc", NULL);
      perror("Failed to exec wc");
   }
   return 1;
}
''', "C pipe dup2 exec ls wc redirect stdin stdout fork lab2"),

    # ─── LAB 2+4: execls.c — fork and exec ls ───────────────────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int  main(void) {
   pid_t childpid;
   childpid = fork();
   if (childpid == -1)  {
       perror("Failed to fork");
       return 1;
   }
   if (childpid == 0) {                            /* child code */
       execl("/usr/bin/ls", "ls", NULL);
       perror("Child failed to exec ls");
       return 1;
   }
   printf("I am so sad my child just died\\n");
   return 0;
}
''', "C fork exec execl child process replace ls lab2"),

    # ─── LAB 3: IPC makefile ─────────────────────────────────────────────
    (r'''all: msgreader.exe msgwriter.exe shmem_writer.exe shmem_reader.exe

msgreader.exe: msgreader.c msgqueue.h
	gcc -o msgreader.exe msgreader.c

msgwriter.exe: msgwriter.c msgqueue.h
	gcc -o msgwriter.exe msgwriter.c

shmem_writer.exe: shmem_writer.c
	gcc -o shmem_writer.exe shmem_writer.c

shmem_reader.exe: shmem_reader.c
	gcc -o shmem_reader.exe shmem_reader.c

clean:
	rm -f *.exe
''', "Makefile IPC message queue shared memory multiple executables lab3"),

    # ─── LAB 6: parentchildfifo.c — FIFO named pipe ─────────────────────
    ('''#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s pipename\\n", argv[0]);
        return 1;
    }
    if (mkfifo(argv[1], S_IRUSR | S_IWUSR) == -1 && errno != EEXIST) {
        perror("mkfifo"); return 1;
    }
    pid_t pid = fork();
    if (pid == 0) {
        // Child writes to FIFO
        int fd;
        while ((fd = open(argv[1], O_WRONLY)) == -1 && errno == EINTR);
        char buf[256];
        snprintf(buf, sizeof(buf), "[%ld]: Hello from child!\\n", (long)getpid());
        write(fd, buf, strlen(buf) + 1);
        close(fd);
        return 0;
    }
    // Parent reads from FIFO
    int fd;
    while ((fd = open(argv[1], O_RDONLY)) == -1 && errno == EINTR);
    char buf[256];
    read(fd, buf, sizeof(buf));
    printf("Parent read: %s\\n", buf);
    close(fd); wait(NULL);
    return 0;
}
''', "C FIFO named pipe mkfifo parent child read write fork lab6"),

    # ─── LAB 7: thread1.c — basic pthread create join ────────────────────
    ('''#include <stdio.h>
#include <pthread.h>

void *myWork(void *arg) {
    int id = *(int *)arg;
    printf("Thread %d running\\n", id);
    return NULL;
}

int main(void) {
    pthread_t tid[3];
    int ids[3] = {0, 1, 2};
    for (int i = 0; i < 3; i++)
        pthread_create(&tid[i], NULL, myWork, &ids[i]);
    for (int i = 0; i < 3; i++)
        pthread_join(tid[i], NULL);
    printf("All threads done\\n");
    return 0;
}
// Compile: gcc -o thread1 thread1.c -lpthread
''', "C pthread create join threads basic example lab7"),

    # ─── LAB 7: PrintThread.c — two threads print A and B ────────────────
    ('''#include <stdio.h>
#include <pthread.h>

pthread_t tid[2];

void *printA(void *arg) { for(int i=0;i<40;i++) printf("A"); return NULL; }
void *printB(void *arg) { for(int i=0;i<40;i++) printf("B"); return NULL; }

int main(void) {
    pthread_create(&tid[0], NULL, printA, NULL);
    pthread_create(&tid[1], NULL, printB, NULL);
    pthread_join(tid[0], NULL);
    pthread_join(tid[1], NULL);
    return 0;
}
// Output shows concurrent interleaving: AABBABABBA...
// Compile: gcc -o PrintThread PrintThread.c -lpthread
''', "C pthread print A B concurrent interleaving threads lab7"),

    # ─── LAB 7: Matrixsquare.c — thread per row ─────────────────────────
    ('''#include <stdio.h>
#include <pthread.h>

pthread_t thread_id[3];

void *square(void *row) {
    int *trow = (int *)row;
    for (int i = 0; i < 3; i++) trow[i] = trow[i] * trow[i];
    return NULL;
}

int main(void) {
    int a[3][3] = {{1,2,3},{3,4,5},{5,6,7}};
    for (int i = 0; i < 3; i++)
        pthread_create(&thread_id[i], NULL, square, a[i]);
    for (int i = 0; i < 3; i++)
        pthread_join(thread_id[i], NULL);
    printf("Squared matrix:\\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) printf("%d ", a[i][j]);
        printf("\\n");
    }
    return 0;
}
// Compile: gcc -o Matrixsquare Matrixsquare.c -lpthread
''', "C pthread matrix squaring thread per row lab7"),

    # ─── LAB 8: sem_setup.c — semaphore create initialize ────────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

#define SEMKEY 456
#define PLAIN 0
#define CHOC 1
#define SHUG 2

union semun { int val; struct semid_ds *buf; unsigned short *array; };

int main(void) {
    int sem_id;
    union semun arg;
    unsigned short dcount[3];

    sem_id = semget(SEMKEY, 3, IPC_CREAT | IPC_EXCL | 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    dcount[PLAIN] = 2;
    dcount[CHOC]  = 3;
    dcount[SHUG]  = 4;
    arg.array = dcount;

    if (semctl(sem_id, 0, SETALL, arg) == -1) {
        perror("semctl"); exit(1);
    }
    printf("Semaphore set created with ID=%d\\n", sem_id);
    return 0;
}
''', "C semaphore semget semctl SETALL create initialize setup lab8"),

    # ─── LAB 8: producer.c — semaphore V operation (produce) ─────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

#define SEMKEY 456
#define PLAIN 0
#define CHOC 1
#define SHUG 2

union semun { int val; struct semid_ds *buf; unsigned short *array; };

int main(void) {
    struct sembuf sops[3];
    union semun arg;
    unsigned short dcount[3];

    int sem_id = semget(SEMKEY, 3, 0666);
    if (sem_id < 0) { perror("Cannot get semaphore"); return 1; }

    arg.array = dcount;
    semctl(sem_id, 0, GETALL, arg);
    printf("Current: Plain %d, Chocolate: %d, Sugar: %d\\n",
           arg.array[PLAIN], arg.array[CHOC], arg.array[SHUG]);

    printf("Enter how many to produce (plain choc sugar): ");
    scanf("%hu %hu %hu", &arg.array[PLAIN], &arg.array[CHOC], &arg.array[SHUG]);

    // V operation: positive sem_op = release/produce
    sops[PLAIN].sem_num = PLAIN; sops[PLAIN].sem_op = arg.array[PLAIN]; sops[PLAIN].sem_flg = 0;
    sops[CHOC].sem_num = CHOC;   sops[CHOC].sem_op = arg.array[CHOC];   sops[CHOC].sem_flg = 0;
    sops[SHUG].sem_num = SHUG;   sops[SHUG].sem_op = arg.array[SHUG];   sops[SHUG].sem_flg = 0;

    if (semop(sem_id, sops, 3) < 0) perror("semop error");
    else {
        semctl(sem_id, 0, GETALL, arg);
        printf("New: Plain: %d, Chocolate: %d, Sugar: %d\\n",
               arg.array[PLAIN], arg.array[CHOC], arg.array[SHUG]);
    }
    return 0;
}
''', "C semaphore producer V operation semop positive release lab8"),

    # ─── LAB 8: consumer.c — semaphore P operation (consume) ─────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

#define SEMKEY 456
#define PLAIN 0
#define CHOC 1
#define SHUG 2

union semun { int val; struct semid_ds *buf; unsigned short *array; };

int main(void) {
    struct sembuf sops[3];
    union semun arg;
    unsigned short dcount[3];

    int sem_id = semget(SEMKEY, 3, 0666);
    if (sem_id < 0) { perror("Cannot get semaphore"); return 1; }

    arg.array = dcount;
    semctl(sem_id, 0, GETALL, arg);
    printf("Current: Plain %d, Chocolate: %d, Sugar: %d\\n",
           arg.array[PLAIN], arg.array[CHOC], arg.array[SHUG]);

    printf("Enter how many to consume (plain choc sugar): ");
    scanf("%hu %hu %hu", &arg.array[PLAIN], &arg.array[CHOC], &arg.array[SHUG]);

    // P operation: negative sem_op = acquire/consume (blocks if insufficient)
    sops[PLAIN].sem_num = PLAIN; sops[PLAIN].sem_op = 0 - arg.array[PLAIN]; sops[PLAIN].sem_flg = 0;
    sops[CHOC].sem_num = CHOC;   sops[CHOC].sem_op = 0 - arg.array[CHOC];   sops[CHOC].sem_flg = 0;
    sops[SHUG].sem_num = SHUG;   sops[SHUG].sem_op = 0 - arg.array[SHUG];   sops[SHUG].sem_flg = 0;

    if (semop(sem_id, sops, 3) < 0) perror("semop error");
    else {
        semctl(sem_id, 0, GETALL, arg);
        printf("New: Plain: %d, Chocolate: %d, Sugar: %d\\n",
               arg.array[PLAIN], arg.array[CHOC], arg.array[SHUG]);
    }
    return 0;
}
''', "C semaphore consumer P operation semop negative acquire lab8"),

    # ─── LAB 9: server.c — TCP socket server ─────────────────────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg) { perror(msg); exit(1); }

int main(int argc, char *argv[]) {
    int sockfd, newsockfd, portno;
    socklen_t clilen;
    char c;
    struct sockaddr_in serv_addr, cli_addr;
    int n;

    if (argc < 2) { fprintf(stderr, "ERROR, no port provided\\n"); exit(1); }

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = portno;

    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)))
        error("ERROR on binding");
    listen(sockfd, 5);
    clilen = sizeof(cli_addr);

    while(1) {
        newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd < 0) error("ERROR on accept");
        do {
            n = read(newsockfd, &c, 1);
            if (n < 0) error("ERROR reading from socket");
            printf("I got: %c\\n", c);
            ++c;
            n = write(newsockfd, &c, 1);
            if (n < 0) error("ERROR writing to socket");
        } while (--c != 'Q');
        close(newsockfd);
    }
}
''', "C socket TCP server bind listen accept read write lab9"),

    # ─── LAB 9: client.c — TCP socket client ─────────────────────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

void error(const char *msg) { perror(msg); exit(0); }

int main(int argc, char *argv[]) {
    char c;
    int sockfd, portno, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;

    if (argc < 3) { fprintf(stderr, "usage %s hostname port\\n", argv[0]); exit(0); }
    portno = atoi(argv[2]);

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    server = gethostbyname(argv[1]);
    if (server == NULL) { fprintf(stderr, "ERROR, no such host\\n"); exit(0); }

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    bcopy((char *)server->h_addr, (char *)&serv_addr.sin_addr.s_addr, server->h_length);
    serv_addr.sin_port = htons(portno);

    if (connect(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
        error("ERROR connecting");

    while(1) {
        printf("Please enter a single char: ");
        c = (char)getc(stdin); getc(stdin);
        n = write(sockfd, &c, 1);
        if (n < 0) error("ERROR writing to socket");
        if (c == '0') { close(sockfd); return 0; }
        n = read(sockfd, &c, 1);
        if (n < 0) error("ERROR reading from socket");
        printf("I got %c from server\\n", c);
    }
}
''', "C socket TCP client connect gethostbyname read write lab9"),

    # ─── LAB 9: server2.c — concurrent server with fork ──────────────────
    ('''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg) { perror(msg); exit(1); }

int main(int argc, char *argv[]) {
    int sockfd, newsockfd, portno;
    socklen_t clilen;
    char c;
    struct sockaddr_in serv_addr, cli_addr;
    int n;
    pid_t pid;

    if (argc < 2) { fprintf(stderr, "ERROR, no port provided\\n"); exit(1); }

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    bzero((char *) &serv_addr, sizeof(serv_addr));
    portno = atoi(argv[1]);
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = INADDR_ANY;
    serv_addr.sin_port = portno;

    if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)))
        error("ERROR on binding");
    listen(sockfd, 5);
    clilen = sizeof(cli_addr);

    while(1) {
        newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd < 0) error("ERROR on accept");

        pid = fork();
        if (pid < 0) error("ERROR in new process creation");
        if (pid == 0) {
            // child process handles this client
            close(sockfd);
            do {
                n = read(newsockfd, &c, 1);
                if (n < 0) error("ERROR reading from socket");
                printf("I got: %c from client\\n", c);
                ++c;
                n = write(newsockfd, &c, 1);
                if (n < 0) error("ERROR writing to socket");
            } while (--c != 'Q');
            close(newsockfd);
            return 0;
        }
        else  // parent process
            close(newsockfd);
    }
    return 0;
}
''', "C socket TCP concurrent server fork per client child process lab9"),

    # ─── LAB 2+4: outputPID.c ────────────────────────────────────────────
    ('''#include <stdio.h>
#include <unistd.h>

int main (void) {
   printf("I am process %ld\\n", (long)getpid());
   printf("My parent is %ld\\n", (long)getppid());
   return 0;
}
''', "C getpid getppid print process ID parent ID lab2"),
]
