"""New data corpus extracted from OS lab exam guides in new_data/."""

NEW_DATA_SNIPPETS = [

    # ─── BASH SCRIPTING ───────────────────────────────────────────────────────

    ('''#!/bin/bash
# LT3 Part A: Organize .txt files by word count into short/ medium/ long/
short_count=0; medium_count=0; long_count=0; total=0
[ ! -d "short" ]  && mkdir short
[ ! -d "medium" ] && mkdir medium
[ ! -d "long" ]   && mkdir long
echo "--- File Organization Started ---"
for file in *.txt; do
    [ ! -f "$file" ] && continue
    words=$(wc -w < "$file")
    total=$((total + 1))
    if [ $words -lt 100 ]; then
        mv "$file" short/
        echo "Moved $file (Words: $words) -> short/"
        short_count=$((short_count + 1))
    elif [ $words -le 500 ]; then
        mv "$file" medium/
        echo "Moved $file (Words: $words) -> medium/"
        medium_count=$((medium_count + 1))
    else
        mv "$file" long/
        echo "Moved $file (Words: $words) -> long/"
        long_count=$((long_count + 1))
    fi
done
echo "--- Summary ---"
echo "Total: $total | Short: $short_count | Medium: $medium_count | Long: $long_count"
''', "bash script organize txt files by word count short medium long directories"),

    ('''#!/bin/bash
# LT3 Part B: sum_of_digits and multiplication_table functions
sum_of_digits() {
    local num=$1
    local sum=0
    while [ $num -gt 0 ]; do
        digit=$((num % 10))
        sum=$((sum + digit))
        num=$((num / 10))
    done
    echo "Sum of digits: $sum"
}

multiplication_table() {
    local num=$1
    echo "Multiplication table of $num:"
    for ((i=1; i<=10; i++)); do
        printf "%d x %2d = %d\n" $num $i $((num * i))
    done
}

read -p "Enter a number: " number
sum_of_digits $number
multiplication_table $number
''', "bash script sum of digits multiplication table functions"),

    ('''#!/bin/bash
# Check if a number is prime
read -p "Enter a number: " num
if [ $num -le 1 ]; then echo "$num is not prime"; exit 0; fi
is_prime=1
for ((i=2; i*i<=num; i++)); do
    if [ $((num % i)) -eq 0 ]; then is_prime=0; break; fi
done
if [ $is_prime -eq 1 ]; then echo "$num is prime"
else echo "$num is not prime"; fi
''', "bash check prime number"),

    ('''#!/bin/bash
# Fibonacci series in bash
read -p "How many terms? " n
a=0; b=1
echo "Fibonacci series:"
for ((i=0; i<n; i++)); do
    echo -n "$a "
    temp=$((a + b)); a=$b; b=$temp
done
echo
''', "bash fibonacci series"),

    ('''#!/bin/bash
# Factorial using bash loop
read -p "Enter a number: " num
fact=1
for ((i=1; i<=num; i++)); do
    fact=$((fact * i))
done
echo "Factorial of $num is $fact"
''', "bash factorial function loop"),

    (r'''#!/bin/bash
# Simple calculator with case statement
read -p "Enter first number: " a
read -p "Enter operator (+, -, *, /): " op
read -p "Enter second number: " b
case $op in
    +) result=$((a + b)) ;;
    -) result=$((a - b)) ;;
    \*) result=$((a * b)) ;;
    /)
        if [ $b -eq 0 ]; then echo "Error: Division by zero"; exit 1; fi
        result=$((a / b)) ;;
    *) echo "Invalid operator"; exit 1 ;;
esac
echo "$a $op $b = $result"
''', "bash simple calculator case statement"),

    ('''#!/bin/bash
# File organizer: move .jpg/.png to images/, .txt/.pdf to documents/
dir=$1
mkdir -p "$dir/images" "$dir/documents"
for file in "$dir"/*; do
    [ ! -f "$file" ] && continue
    case "$file" in
        *.jpg|*.png) mv "$file" "$dir/images/" ; echo "Moved $file -> images/" ;;
        *.txt|*.pdf) mv "$file" "$dir/documents/" ; echo "Moved $file -> documents/" ;;
    esac
done
''', "bash file organizer move jpg png txt pdf directories"),

    ('''#!/bin/bash
# Number guessing game with hints
secret=$((RANDOM % 10 + 1))
echo "Guess a number between 1 and 10:"
while true; do
    read guess
    if [ $guess -lt $secret ]; then echo "Too low!"
    elif [ $guess -gt $secret ]; then echo "Too high!"
    else echo "Correct! The number was $secret"; break
    fi
done
''', "bash number guessing game random hints"),

    ('''#!/bin/bash
# Read file line by line and check existence
while IFS= read -r file; do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        echo "$file exists — Size: $size bytes"
    else
        echo "$file: File not found"
    fi
done < files_to_check.txt
''', "bash read file line by line check exists"),

    ('''#!/bin/bash
# Find largest file in a directory
dir=${1:-.}
largest=""; max_size=0
for file in "$dir"/*; do
    if [ -f "$file" ]; then
        size=$(wc -c < "$file")
        if [ $size -gt $max_size ]; then
            max_size=$size; largest=$file
        fi
    fi
done
echo "Largest file: $largest ($max_size bytes)"
''', "bash find largest file directory"),

    ('''#!/bin/bash
# Backup script with timestamp
src=$1; dest=$2
date_str=$(date +%Y%m%d_%H%M%S)
backup_name="${dest}/backup_${date_str}.tar.gz"
tar -czf "$backup_name" "$src"
echo "Backup created: $backup_name"
''', "bash backup script tar timestamp"),

    ('''#!/bin/bash
# Check disk usage and alert if above threshold
threshold=80
usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $usage -gt $threshold ]; then
    echo "WARNING: Disk usage is ${usage}% (above ${threshold}%)"
else
    echo "OK: Disk usage is ${usage}%"
fi
''', "bash check disk usage alert threshold"),

    ('''#!/bin/bash
# Odd/Even summer: sum of odd and even numbers from 1 to N
read -p "Enter N: " N
even_sum=0; odd_sum=0
for ((i=1; i<=N; i++)); do
    if [ $((i % 2)) -eq 0 ]; then even_sum=$((even_sum + i))
    else odd_sum=$((odd_sum + i)); fi
done
echo "Sum of even numbers: $even_sum"
echo "Sum of odd numbers: $odd_sum"
''', "bash odd even sum numbers loop"),

    ('''#!/bin/bash
# Rename all files in directory with prefix
prefix=$1
for file in *; do
    if [ -f "$file" ]; then
        mv "$file" "${prefix}_${file}"
        echo "Renamed: $file -> ${prefix}_${file}"
    fi
done
''', "bash rename files add prefix"),

    ('''#!/bin/bash
# Reverse a string in bash
read -p "Enter a string: " str
echo "$str" | rev
# Manual reverse:
len=${#str}; reversed=""
for ((i=len-1; i>=0; i--)); do
    reversed="$reversed${str:$i:1}"
done
echo "Reversed: $reversed"
''', "bash reverse string"),

    # ─── FORK / PIPES / MESSAGE QUEUES ───────────────────────────────────────

    ('''#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

// Basic fork() pattern — parent and child
int main(void) {
    pid_t childpid = fork();
    if (childpid == -1) { perror("fork failed"); return 1; }
    if (childpid == 0) {
        printf("CHILD: PID=%ld, Parent=%ld\\n", (long)getpid(), (long)getppid());
        return 0;
    }
    printf("PARENT: PID=%ld, Child=%ld\\n", (long)getpid(), (long)childpid);
    wait(NULL);
    printf("PARENT: Child has finished\\n");
    return 0;
}
''', "C fork process parent child wait"),

    ('''#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

// Fan topology: one parent, N children (child breaks from loop)
int main(int argc, char *argv[]) {
    int n = 4;
    pid_t childpid = 0;
    for (int i = 1; i < n; i++) {
        if ((childpid = fork()) <= 0) break; // child breaks out
    }
    if (childpid == 0)
        printf("CHILD PID=%ld\\n", (long)getpid());
    else {
        for (int i = 1; i < n; i++) wait(NULL);
        printf("PARENT: all children done\\n");
    }
    return 0;
}
''', "C fork fan topology multiple children"),

    ('''#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

// Chain topology: each process creates next (parent breaks)
int main(int argc, char *argv[]) {
    int n = 4;
    pid_t childpid;
    for (int i = 1; i < n; i++) {
        if (childpid = fork()) break; // parent breaks, child continues
    }
    printf("PID=%ld PPID=%ld\\n", (long)getpid(), (long)getppid());
    wait(NULL);
    return 0;
}
''', "C fork chain topology process tree"),

    ('''#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

// Pipe: parent writes, child reads
int main(void) {
    int fd[2];  // fd[0]=read, fd[1]=write
    pipe(fd);
    pid_t pid = fork();
    if (pid == 0) {
        // CHILD reads
        close(fd[1]);
        char buf[100];
        read(fd[0], buf, sizeof(buf));
        printf("Child received: %s\\n", buf);
        close(fd[0]);
        return 0;
    }
    // PARENT writes
    close(fd[0]);
    char *msg = "Hello child!";
    write(fd[1], msg, strlen(msg) + 1);
    close(fd[1]);
    wait(NULL);
    return 0;
}
''', "C pipe parent write child read communication"),

    ('''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/wait.h>

// Message queue: struct + msgsnd + msgrcv
struct msg { long type; int pid; int sum; };

int main(void) {
    int msgid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);
    pid_t pid = fork();
    if (pid == 0) {
        struct msg m;
        m.type = 1; m.pid = getpid(); m.sum = 42;
        msgsnd(msgid, &m, sizeof(m) - sizeof(long), 0);
        return 0;
    }
    wait(NULL);
    struct msg m;
    msgrcv(msgid, &m, sizeof(m) - sizeof(long), 1, 0);
    printf("From PID %d: sum = %d\\n", m.pid, m.sum);
    msgctl(msgid, IPC_RMID, NULL);
    return 0;
}
''', "C message queue msgget msgsnd msgrcv IPC"),

    ('''#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/msg.h>

// LT2 full solution: pipe + message queue + 4 children
struct msg { long type; int pid; int sum; };

int main(void) {
    int pipefd[2]; int numbers[40]; int total = 0;
    pipe(pipefd);
    int msgid = msgget(IPC_PRIVATE, 0666 | IPC_CREAT);

    printf("Parent %ld writing 40 numbers\\n", (long)getpid());
    for (int i = 0; i < 40; i++) {
        numbers[i] = rand() % 100;
        total += numbers[i];
        printf("%d ", numbers[i]);
    }
    printf("\\nTotal sum: %d\\n", total);
    write(pipefd[1], numbers, sizeof(numbers));
    close(pipefd[1]);

    for (int i = 0; i < 4; i++) {
        if (fork() == 0) {
            int arr[10]; read(pipefd[0], arr, sizeof(arr));
            int sum = 0;
            for (int j = 0; j < 10; j++) sum += arr[j];
            struct msg m; m.type = 1; m.pid = getpid(); m.sum = sum;
            msgsnd(msgid, &m, sizeof(m) - sizeof(long), 0);
            exit(0);
        }
    }
    close(pipefd[0]);
    for (int i = 0; i < 4; i++) {
        struct msg m;
        msgrcv(msgid, &m, sizeof(m) - sizeof(long), 1, 0);
        printf("PID %d sum of 10 numbers: %d\\n", m.pid, m.sum);
    }
    for (int i = 0; i < 4; i++) wait(NULL);
    msgctl(msgid, IPC_RMID, NULL);
    return 0;
}
''', "C fork pipe message queue LT2 children sum IPC"),

    ('''#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>

// dup2: redirect stdout to file
int main(void) {
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_APPEND, S_IRUSR | S_IWUSR);
    dup2(fd, STDOUT_FILENO);   // stdout now goes to output.txt
    close(fd);
    write(STDOUT_FILENO, "This goes to file!\\n", 19);
    return 0;
}
''', "C dup2 redirect stdout file"),

    ('''#include <stdio.h>
#include <unistd.h>
// exec: replace process with new program
int main(void) {
    pid_t pid = fork();
    if (pid == 0) {
        execl("/bin/ls", "ls", "-l", NULL);
        perror("exec failed");
        return 1;
    }
    wait(NULL);
    return 0;
}
''', "C exec execl fork replace process"),

    # ─── MAKEFILE ────────────────────────────────────────────────────────────

    ('''# Makefile: build executable from multiple .c files
CC = gcc
CFLAGS = -Wall -g

myprogram: main.o utils.o
\t$(CC) $(CFLAGS) -o myprogram main.o utils.o

main.o: main.c utils.h
\t$(CC) $(CFLAGS) -c main.c

utils.o: utils.c utils.h
\t$(CC) $(CFLAGS) -c utils.c

clean:
\trm -f *.o myprogram
''', "Makefile build multiple c files executable clean"),

    ('''# Makefile: static and shared libraries
test: main.o libmystaticlib.a libmysharedlib.so
\tgcc -o test main.o -L. -lmystaticlib -lmysharedlib

main.o: main.c myheader.h
\tgcc -c main.c

f1.o: f1.c
\tgcc -c f1.c

f2.o: f2.c
\tgcc -c -fpic f2.c

libmysharedlib.so: f2.o
\tgcc -shared -o libmysharedlib.so f2.o

libmystaticlib.a: f1.o
\tar cr libmystaticlib.a f1.o

clean:
\trm -f *.o libmystaticlib.a libmysharedlib.so test
''', "Makefile static shared library ar gcc fpic"),

    ('''# Makefile: build server and client executables
all: server client

server: server.c common.h
\tgcc -o server server.c

client: client.c common.h
\tgcc -o client client.c

clean:
\trm -f server client
''', "Makefile server client build executables"),

    ('''# Makefile: multiple IPC executables (Lab 3 style)
all: msgreader.exe msgwriter.exe shmem_writer.exe shmem_reader.exe

msgreader.exe: msgreader.c msgqueue.h
\tgcc -o msgreader.exe msgreader.c

msgwriter.exe: msgwriter.c msgqueue.h
\tgcc -o msgwriter.exe msgwriter.c

shmem_writer.exe: shmem_writer.c
\tgcc -o shmem_writer.exe shmem_writer.c

shmem_reader.exe: shmem_reader.c
\tgcc -o shmem_reader.exe shmem_reader.c

clean:
\trm -f *.exe
''', "Makefile multiple executables IPC message queue shared memory"),

    # ─── PTHREADS ────────────────────────────────────────────────────────────

    ('''#include <stdio.h>
#include <pthread.h>

// Basic pthreads: create and join threads
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
// Compile: gcc -o out file.c -lpthread
''', "C pthreads pthread_create pthread_join thread"),

    ('''#include <stdio.h>
#include <pthread.h>

// Thread matrix squaring (each thread squares one row)
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
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) printf("%d ", a[i][j]);
        printf("\\n");
    }
    return 0;
}
''', "C pthread matrix squaring thread per row"),

    ('''#include <stdio.h>
#include <pthread.h>

// PrintAB: two threads print A and B concurrently
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
// Output: AABBABABBAABB... (concurrent interleaving)
''', "C pthread print A B concurrent threads"),

    # ─── SEMAPHORES ──────────────────────────────────────────────────────────

    ('''#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

// Semaphore setup: create and initialize (P=acquire negative, V=release positive)
#define SEMKEY 456
union semun { int val; struct semid_ds *buf; unsigned short *array; };

int main(void) {
    int sem_id = semget(SEMKEY, 3, IPC_CREAT | IPC_EXCL | 0666);
    if (sem_id < 0) { perror("semget"); exit(1); }

    union semun arg;
    unsigned short counts[3] = {2, 3, 4}; // initial values
    arg.array = counts;
    semctl(sem_id, 0, SETALL, arg);
    printf("Semaphore set created. ID=%d\\n", sem_id);
    return 0;
}
''', "C semaphore semget semctl SETALL create initialize"),

    ('''#include <sys/sem.h>
#include <stdio.h>

// Semaphore P (acquire/down, negative) and V (release/up, positive)
// P operation: sem_op = -N (blocks if would go negative)
// V operation: sem_op = +N (releases waiting processes)
void P(int sem_id, int sem_num) {
    struct sembuf op = {sem_num, -1, 0};
    semop(sem_id, &op, 1);
}

void V(int sem_id, int sem_num) {
    struct sembuf op = {sem_num, +1, 0};
    semop(sem_id, &op, 1);
}
''', "C semaphore P V operation acquire release semop"),

    # ─── SHARED MEMORY ───────────────────────────────────────────────────────

    ('''#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/stat.h>
#include <stdio.h>
#include <unistd.h>

// Shared memory: create, attach, write, detach, delete
int main(void) {
    key_t key = ftok("/etc/passwd", 5);
    int shm_id = shmget(key, 100, S_IRUSR | S_IWUSR | IPC_CREAT);
    char *ptr = (char *)shmat(shm_id, NULL, 0);

    sprintf(ptr, "Hello from PID %ld", (long)getpid());
    printf("Wrote: %s\\n", ptr);

    shmdt(ptr);
    shmctl(shm_id, IPC_RMID, NULL);
    return 0;
}
''', "C shared memory shmget shmat shmdt shmctl IPC"),

    # ─── FIFO / NAMED PIPES ──────────────────────────────────────────────────

    ('''#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/wait.h>

// FIFO named pipe: mkfifo + parent-child communication
int main(int argc, char *argv[]) {
    if (argc != 2) { fprintf(stderr, "Usage: %s pipename\\n", argv[0]); return 1; }

    if (mkfifo(argv[1], S_IRUSR | S_IWUSR) == -1 && errno != EEXIST) {
        perror("mkfifo"); return 1;
    }
    pid_t pid = fork();
    if (pid == 0) {
        // Child writes
        int fd;
        while ((fd = open(argv[1], O_WRONLY)) == -1 && errno == EINTR);
        char buf[256];
        snprintf(buf, sizeof(buf), "[%ld]: Hello from child!\\n", (long)getpid());
        write(fd, buf, strlen(buf) + 1);
        close(fd);
        return 0;
    }
    // Parent reads
    int fd;
    while ((fd = open(argv[1], O_RDONLY)) == -1 && errno == EINTR);
    char buf[256];
    read(fd, buf, sizeof(buf));
    printf("Parent read: %s\\n", buf);
    close(fd); wait(NULL);
    return 0;
}
''', "C FIFO named pipe mkfifo parent child communication"),

    # ─── SOCKETS ─────────────────────────────────────────────────────────────

    ('''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

// TCP concurrent server: socket bind listen accept fork per client
int main(void) {
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(5000);

    bind(listenfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    listen(listenfd, 10);
    printf("Server listening on port 5000...\\n");

    while (1) {
        int connfd = accept(listenfd, NULL, NULL);
        pid_t pid = fork();
        if (pid == 0) {
            close(listenfd);
            char buf[1024] = {0};
            read(connfd, buf, sizeof(buf));
            printf("Client says: %s\\n", buf);
            write(connfd, "Hello from server!", 18);
            close(connfd); exit(0);
        }
        close(connfd);
    }
    return 0;
}
''', "C socket TCP server bind listen accept fork concurrent"),

    ('''#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

// TCP client: socket connect write read
int main(void) {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(5000);
    serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
    write(sockfd, "Hello from client", 17);

    char buf[1024] = {0};
    read(sockfd, buf, sizeof(buf));
    printf("Server replied: %s\\n", buf);
    close(sockfd);
    return 0;
}
''', "C socket TCP client connect send receive"),
]
