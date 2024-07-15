# Bash Techniques

## Variables 

If `variable1` is the name of a variable, then `$variable1` is a reference to its value, the data item it contains.

```bash
variable1=23
echo variable1
echo $variable1
```

No space permitted on either side of = sign when initializing variables. What happens if there is a space?

```bash
# bad examples 

VARIABLE =value
VARIABLE= value
VARIABLE = value
```

Below are a few examples of variable referencing.
Try them out and make sure you understand each one of the cases.

```bash
HELLO=Hi

echo HELLO      # HELLO
echo $HELLO     # Hi
echo ${HELLO}   # Hi
echo "$HELLO"   # Hi
echo "${HELLO}" # Hi
echo "$HELLO, I like them squishy"
       
# Variable referencing disabled (escaped) by single quotes
echo '$HELLO'
```

There are [MUCH more](https://tldp.org/LDP/abs/html/parameter-substitution.html#PARAMSUBREF) functionalities.

## Script positional variables

Positional arguments are arguments passed to a command or script in a specific order, usually separated by spaces. Positional arguments can be accessed, within a bash script file, using special variables such as `$1`, `$2`, `$3`, and so on, where `$1` refers to the first argument, `$2` refers to the second argument, and so on.

Let's see them in action... create a file called `BarackObama.sh` as follows:

```bash
#!/bin/bash

# This script reads 3 positional parameters and prints them out.

echo "$0 invoked with the following arguments: $@"

POSPAR1="$1"
POSPAR2="$2"
POSPAR3="$3"

echo "$1 is the first positional parameter, \$1."
echo "$2 is the second positional parameter, \$2."
echo "$3 is the third positional parameter, \$3."
echo
echo "The total number of positional parameters is $#."

if [ -n "${10}" ]               # Parameters > $9 must be enclosed in {brackets}.
then
  echo "Parameter #10 is ${10}"
fi
```

Execute the script by:

```bash
bash positional.sh Yes We Can 
bash positional.sh Yes We Can bla bla 1 2 3
```

Investigate the script output and make sure you understand each variable. 

## Exit status and `$?`

In Unix-like operating systems, every command that is executed returns an exit status to the shell that invoked it. The exit status is a numeric value that indicates the success or failure of the command. A value of 0 indicates success, while a non-zero value indicates failure.

The exit status of the most recently executed command can be accessed via the `$?` variable in Bash.

```console
[myuser@hostname]~$ ls /non-existing-dir
ls: cannot access '/non-existing-dir': No such file or directory
[myuser@hostname]~$ echo $?
2
```

In the above example, if you run a command like `ls /non-existing-dir`, you will receive an error message saying that the directory does not exist, and the exit status will be non-zero. You can access the exit status of this command by typing `echo $?`. The output will be the exit status of the previous command (in this case, the value is 2).
Some common non-zero exit status values include:

- `1`: General catch-all error code
- `2`: Misuse of shell built-ins (e.g. incorrect number of arguments)
- `126`: Command found but not executable
- `127`: Command not found
- `128`+: Exit status of a program that was terminated due to a signal


Explore the man page of the `grep` command. List all possible exit codes, and specify the reason for every exit code.

## Running Multiple Commands (Conditionally)

The bash shell allows users to join multiple commands on a single command line by separating the commands with a `;` (semicolon).

```console
[myuser@hostname]~$ cd /etc/ssh; ls
moduli  	ssh_config.d  sshd_config.d   	ssh_host_ecdsa_key.pub  ssh_host_ed25519_key.pub  ssh_host_rsa_key.pub
ssh_config  sshd_config   ssh_host_ecdsa_key  ssh_host_ed25519_key	ssh_host_rsa_key      	ssh_import_id
[myuser@hostname]/etc/ssh$
```

Nothing special in the above example… just two commands that were executed one after the other. 

The bash shell uses `&&` and `||` to join two commands conditionally. When commands are conditionally joined, the first will always execute. The second command may execute or not, depending on the return value (exit code) of the first command. For example, a user may want to create a directory, and then move a new file into that directory. If the creation of the directory fails, then there is no reason to move the file. The two commands can be coupled as follows:

```console
[myuser@hostname]~$ echo "one two three" > numbers.txt
[myuser@hostname]~$ mkdir /tmp/boring && mv numbers.txt /tmp/boring
```

By coupling two commands with `&&`, the second command will only run if the first command succeeded (i.e., had a return value of 0).

What if the `mkdir` command failed?

Similarly, multiple commands can be combined with `||`. In this case, bash will execute the second command only if the first command "fails" (has a non zero exit code). This is similar to the "or" operator found in programming languages. In the following example, myuser attempts to change the permissions on a file. If the command fails, a message to that effect is echoed to the screen.

```console
[myuser@hostname]~$ chmod 600 /tmp/boring/numbers.txt || echo "chmod failed."
[myuser@hostname]~$ chmod 600 /tmp/mostly/boring/primes.txt || echo "chmod failed"
chmod: failed to get attributes of /tmp/mostly/boring/primes.txt': No such file or directory
chmod failed
```

It’s common in bash scripts to create a directory and immediately `cd` to the directory, if the creations succeeded. Use conditional the `&&` operator to create the dir and cd into it only if the creation succeeded. 

<details>
  <summary>
     Solution
  </summary>

```bash
mkdir newdir && cd newdir
```

</details>

## Command Substitution

Command substitution allows users to run arbitrary commands in a subshell and incorporate the results into the command line. The modern syntax supported by the bash shell is: 

```bash
$(subcommand)
```

As an example of command substitution, `myuser` would like to create a directory that contains the date in its name. After examining the `date(1)` man page, he devises a format string to generate the date in a compact format.

```bash
[prince@station prince]$ date +%d%b%Y
04May2023
```

He now runs the mkdir command, using command substitution.

```bash
[prince@station prince]$ mkdir reports.$(date +%d%b%Y)
[prince@station prince]$ ls
reports.04May2003
```

The bash shell implements command substitution by spawning a new subshell, running the command, recording the output, and exiting the subshell. The text used to invoke the command substitution is then replaced with the recorded output from the command.

## Testing files

**Before you start, review the man page of the `test` command.**

The first example checks for the existence of a file:

```bash
echo "This script checks the existence of the messages file."
echo "Checking..."
if [ -f /var/log/messages ]
then
  echo "/var/log/messages exists."
fi
echo
echo "...done."
```


> 🧐 What is the relation between the `test` command and `[`?

## Testing Exit Status

Recall that the $? variable holds the exit status of the previously executed command. The following example utilizes this variable to make a decision according to the success or failure of the previous command:

```bash
curl google.com &> /dev/null

if [ $? -eq 0 ]
then
  echo "Request succeeded"
else
  echo "Request failed, trying again..."
fi
```

# Exercises

### :pencil2: Availability test script

The `curl` command can be used to perform a request to an external website and return the response's [status code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status): 

```bash
curl -o /dev/null -s -w "%{http_code}" www.google.com
```

This `curl` command suppresses output (`-o /dev/null`), runs silently without printing the traffic progress (`-s`), and prints the HTTP status code (`-w "%{http_code}"`).

Create an `availability_test.sh` script that receives an address as the 1st (and only) argument, and perform the above `curl` command. 
The script should be completed successfully if the returned HTTP status code is `< 500`, 
or fail otherwise (you can exit the script with `exit 1` to indicate failure). 

Here is the expected behaviour:

```console
myuser@hostname:~$ ./availability_test.sh www.google.com
www.google.com is up!
myuser@hostname:~$ ./availability_test.sh http://cnn.com
http://cnn.com is up!
myuser@hostname:~$ ./availability_test.sh abcdefg
abcdefg is not available.
myuser@hostname:~$ echo $?
1
myuser@hostname:~$ ./availability_test.sh
A valid URL is required
myuser@hostname:~$ ./availability_test.sh google.com cnn.com
The script is expected a single argument only, but got 2.
myuser@hostname:~$ ./availability_test.sh httpbin.org/status/500   # this url should return a status code of 500
httpbin.org/status/500 is not available.
```

### :pencil2: Geo-location info

Write a bash script `geo_by_ip.sh` that, given an ip address, prints geo-location details, as follows:
1. The script first checks if `jq` cli is installed. If not installed, it prints a message to the user with a link to download the tool: https://stedolan.github.io/jq/download/
1. The script checks that **exactly one argument** was sent to it, which represents the ip address to check. Otherwise, an informative message is printed to stdout.
1. The script checks that the given IP argument is not equal to `127.0.0.1`.
1. The script performs an HTTP GET request to `http://ip-api.com/json/<ip>`, where `<ip>` is the IP argument. The results should be stored in a variable.
1. Using the jq tool and the variable containing the HTTP response, check that the request has succeeded by checking that the `status` key has a value of `success`. The command `jq -r '.<key>'` can extract a key from the json (e.g. `echo $RESPONSE | jq -r '.status'`)
1. If the request succeed, print the following information to the user:
    - country
    - city
    - regionName


### :pencil2: Theater night out booking system

In our course repo, copy the file under `theatre_nighout/init.sh` into an empty directory and execute it.
This script creates 5 directories, each for a famous theater show. 
In each directory there are 50 files, representing 50 available seats for the show.
Create a bash script `available_seat.sh` that takes one argument which is the name of a show and prints the available seats for the show (by simply using `ls` command).
Create another bash script `booking.sh` that takes two arguments - the name of a show and a seat number. 

The selected seat should be marked as booked by deleting the file that represents the seat number.
You should print an informative message to the user upon successful or failed booking.

You can always re-run `init.sh` to test your script again. 

For example:

```console
$ ./init.sh && cd shows
$ ./available_seat.sh Hamilton
Available seats for Hamilton:
1 2 3 4 5 6 7 8 9 10 ... 48 49 50
$ ./booking.sh Hamilton 5
Seat 5 for Hamilton has been booked!
$ ./available_seat.sh Hamilton
Available seats for Hamilton:
1 2 3 4 6 7 8 9 10 ... 48 49 50
$ ./booking.sh Hamilton 5
Error: Seat 5 for Hamilton is already booked!
```

