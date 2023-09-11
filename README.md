# ISP Connection Tool
## Status: In Development
This tool is currently in development. Currently, all functionalities are implemented, 
but it has to be tested and the documentation is missing in some modules.
---
## Description
This tool checks your internet connection every **n** minutes or hours. 
If the connection is down, it tracks the downtime and writes the result into a CSV file.
The intention of the tool is, to have a yearly report of your overall internet availability.  

Keep in mind, that your internet downtime could have many reasons. Not all of them are tied to your ISP.

### Technical Description
Basically it performs a scan on port 80 of **n** hosts.
You can define the hosts in the **/core/config.py** at the variable **HOSTS**.  
By default there are 3 hosts defined in the list, but you can use any amount of hosts.
I recommend to choose hosts, that are not hosted on the same CDN.  

You can check the CDN of a host with the Linux command:
```commandline
host -C duckduckgo.com
```
> duckduckgo.com has SOA record **dns1.p05.nsone.net**

And one example with a site, hosted on Cloudflare:
```commandline
host -C x.com
```
> x.com has SOA record **alexia.ns.cloudflare.com**

### Ping vs Port Scan
Using Ping has the big disadvantage, that servers could be configured to block ping requests.
So you end up with a false-negative response.  
Performing a explicit scan on port 80 - where the HTTP stream goes through - should not result into
false-negative responses.
---

## Dependencies
- Python 3 (Standard Libraries)
- Docker (if you want to use it inside a container)

---
## Usage
### Docker
If you want to build a Docker image, you have to perform some steps in advance, before you can build it with the
contained **Dockerfile**.  

1. **/core/config.py** -> Change the variable **docker_conf** to **True**
2. **./Dockerfile** -> (Optional) Define the environment variables to your needs

### Environment Variables

| Env var            | Value                      | Limits     |
|--------------------|----------------------------|------------|
| TIME_INTERVAL      | integer (Minutes)          | 1-12, 1-30 |
| TIME_MODE          | D or H                     | -          |
| TIME_TOLERANCE     | integer (Minutes)          | see below  |
| MAIN_ROUTINE_SLEEP | integer (Iterations)       | -          |
| SUB_ROUTINE_SLEEP  | integer (Iterations)       | -          |
| SUB_RATE           | integer or float (Seconds) | see below  |

### Explanation
**1. TIME_INTERVAL** & **TIME_MODE**  
You can choose how often per hour or per day it should perform a scan. 
If you wish to do a scan 4 times an hour the variables should be set like:
```dockerfile
ENV TIME_INTERVAL=4
ENV TIME_MODE=H
```
Or 8 times a day:
```dockerfile
ENV TIME_INTERVAL=8
ENV TIME_MODE=D
```

There is one **caveat**: at some configurations (like 7 times per day) it performs a scan at:  
*03:00, 06:00, 09:00, 12:00, 15:00, 18:00 and 21:00* but skips *00:00*.  
I explained the mechanic here: **/core/timeutils.py - method: divide_clock()**.  

**Limits**  
There are boundaries to the values, so there's no weird behavior and collisions.  

| Condition        | Limit  |
|------------------|--------|
| if TIME_MODE = D | 1 - 12 |
| if TIME_MODE = H | 1 - 30 |

**2. TIME_TOLERANCE**  
If a portscan gets performed on 14:00 and something random happens (OS conflicts or some unexpected behaviour),
the scan would be skipped.  
To counter this issue, a tolerance is implemented.  
Additionally this enables the possibility to alter the routine delay times, so nothing overlaps and results in conflicts.

**3. MAIN_ROUTINE_SLEEP** & **SUB_ROUTINE_SLEEP** & **SUB_RATE**  
The main module contains two routines:  
- The main routine: performs a check if the desired time (related to **TIME_INTERVAL**) is reached and
  calls the sub routine if all hosts are offline
- The sub routine: checks if at least one of the hosts is online

Each routine has a sleep timer, so it doesn't waste resources on checking the ports again.  
So basically you can modify each routine's delay. But the delay value isn't in seconds, it's in *iterations*.  
The reason is for receiving signals (like SIGINT & SIGTERM) immediately, and not till the delay of a routine is done.
And that's why **SUB_RATE** comes into play. This defines how long a "second" in a routine delay really is.  

If you define **SUB_RATE=1.5** and **MAIN_ROUTINE_SLEEP=30**, the main routine delay is 30*1.5=45 seconds long.

---
### Without Docker
For using it without Docker, check the config file first:
- **/core/config.py** -> The variable **docker_conf** should be **False**

After that change the time values to your needs. More information about the time values, 
read the section "Environment Variables".

Now just start the **./main.py** file.
```commandline
python main.py
```

---
## Tests
There are test in **/core/tests/**. You can run it via the **run_tests.cmd** or **run_tests.sh** file.
