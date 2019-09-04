# Three Tier ESP Testbed Tower

Various research activities require the programming of a large numbers of devices.  This programming can be difficult to co-ordinate and organise, and requires considerable labour time. These issues often mean that testing on real hardware is abandoned or taken only to small scale implementation thus limiting the real-world findings. The method described in the paper 'A Three Tier Rapid Mass Programming Method', adopts a three tiered approach to programming large numbers of devices. Tier 1 is comprised of a single Master Controller which is networked to individual tower modules, these towers form the final 2 tiers with the Local Controller as tier 2 and up-to 15 target devices forming tier 3. The Master Controller co-ordinates and distributes the code for each device to the Local Controller which then programs the target devices. In the domain of networking this allows for:

	
	* Large networks of varied protocols to be programmed quickly, since towers are programmed in parallel, additional towers don't extend programming times.
	
	* Distributed networks are possible since towers are controlled over Ethernet.
	
	* Low cost as each tower costs around  ~$110 USD.
	
	* Dramatically reduced labour time and defect rates due to human error in setting up devices.

This project implements this method for IoT Networking research with ESP-01 Target devices, including both hardware and software implementations.
Please see the Wiki for instructions on [Configuring a Tower](https://bitbucket.org/tylersteane/three-tier-esp-testbed-tower/wiki/Configuring%20a%20Tower%20Controller)

# Acknowledgement

This work is presented in the research paper : A Three Tier Rapid Mass Programming Method.
As originally proposed and envisioned by Tyler Steane, with technical work completed by Micheal Trifilo (software) & Christopher Rogash (hardware) as over seen by Tyler Steane & Dr. PJ Radcliffe.

# Citation
Please make use of this project in any of your own work (See LICENSE.MIT), If using any part of this work please cite as:

T. Steane, M. Trifilo, C. Rogash and PJ Radcliffe, "A Three Tier Rapid Mass Programming Method", 2019, unpublished.
