# ntnx-escape-game
Roleplay to discover Nutanix platform

# Preparation
- Book a HPOC with following characteristics : 
    - Multinode-cluster
    - AOS 7 <- May need manual update
    - PC2024.3 <- May need manual update
    - Self-Service enabled
    - Leap Enabled
    - Flow security enabled
    - Files with old version 4.x
- prepare your sendgrid token.
  - If you do not have one, create an account and get a token.
- Upload the runbook  `blueprint/EG-prerequisites.json` in the `lab` project
- Launch it
- Upload the blueprint `blueprint/EG-EscapeGame.json` in the `lab` project (wARNING : Ensure you have launched the runbook first or you'll have problems)
- Update NUTANIX credential with password `nutanix/4u`
- Select cluster and primary Network
- Launch it

!! IMPORTANT !! Known Issues : 
 - The current deployemnt as a little problem. Please update manually the project `production` to remove then re-add the user `thebadguy`
 - Please confirm the cluster has only 3 nodes (I experienced an issue once). If not, please remove 4th node.

# Player prerequisites
- Players need to have VPN access to HPOC (is going to be updated and use VDI for a more convenient approach)

# Game launch
- Use Day 2 action of the BP to :
  - Start web services
  - Launch invitation email to your players (you'll have to enter recipients list)
  - Launch "End of lab" email (1st recipients list will be used)

Self Service Application description will provide URL to play, as it will mentioned in the invitation email too.

