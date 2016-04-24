# goaway
distributed computing with flexible consistency models

# Directory Organization
goaway repo:
- README.md (This readme file)
- goaway (Library code)
- examples (Example usage and demos)
- misc (Miscellaneous experiments)
- tests (Tests for library)
# Initialization
 - goaway expects users to define $GOAWAYPATH, which is the path to the application and goaway library. For now these two folders are in the same directory.
 - If you wish to automate the startup of your remote machines, your remote machines must allow you to have ssh access. Otherwise, you will have to manually run
   cmdserver on each machine
# Config file
 - goaway reads from a config file to determine where the goaway application is, and the names of the remote servers.
 - Same config.yaml file:
   `
   ---
   servers: 
     - localhost:9060
     - username@remote.ip.address:portNumber
   filepaths:
     - $GOAWAYPATH/ $GOAWAYPATH/target/machine/file/path
   modules:
     - application_module $GOAWAYPATH/application_module
   `

