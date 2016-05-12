# goaway
distributed computing with flexible consistency models

For a full description, [read the paper](https://github.com/anpere/goaway/raw/master/GoAway.pdf) or [see the slides](https://github.com/anpere/raw/master/GoAway-slides.pdf).

# Directory Organization
- `goaway` - Library code
- `examples` - Example usage and demos. All of the examples assume you have a working config file named remote.yaml.

# Setup
On each computer in the cluster (spawner and remotes), you need to:
- clone this repo and `cd` into the `goaway` folder
- ` sudo pip install -r requirements.txt `
- ` sudo python setup.py develop `

The spawner needs to have SSH access to the remotes (to send code), and all computers need to be able to run a publicly-accessible HTTP server (so no NAT/firewall).

Fill in your [config file](https://github.com/anpere/goaway/blob/master/examples/example.yaml) with the correct information.

# Usage
Check out the `examples` folder for a bunch of demo programs!
