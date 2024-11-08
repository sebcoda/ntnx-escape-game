# Prerequisites
[x] HPOC with 3 nodes, Self service activated


# Deployment of
[] Remove 1 host
[] Check new node is available with command 'api/clustermgmt/v4.0.b2/config/clusters/%s/rackable-units'
[] Activate flow
[] Activate Intelligent Ops
[] Enable DR
[] Deploy PolicyEngine x.x.x.50
[] Create user thebadguy/MyProdPassword in the AD
[] Project 'Production' with cluster and thebadguy as admin
[] 2/3 VMs into this project
[] Create 3 local users (Charlie, Thom and William)
[] Launch Inventory
[] Deploy Clone BP
  [] Create /home/nutanix/.calm/venv 
    [] Install apt install python3.10-venv python3-pip -y
    [] mkdir -p /home/nutanix/.calm
    [] Execute cd /home/nutanix/.calm && python3 -m venv venv
    [] Execute pip install dotenv ntnx_networking_py_client ntnx_vmm_py_client ntnx_prism_py_client
    [] source venv/bin/activated
    [] pip install python-dotenv ntnx_networking_py_client ntnx_vmm_py_client ntnx_prism_py_client
  [] Upload
  [] Change Credential
  [] Create endpoint (on game VM) ? It may keep endpoint if one exists with the good name ? 
  [] Update variables
  [] Updates tasks using endpoint


# Notes :
