
**
junos-pyez
----------
**
NetOps scripts based on Junos PyEZ

There are a few Python scripts created by using custom Junos PyEZ Operational & Configuration Tables and Views which may help with checking the consistency of configuration applied on two MPLS-PE routers.

 
 **StatticRouteCheck**
 ----------
This script is intended to be used for comparing the static routes and their next-hops defined under routing instance configuration stanza between two routers. Missing or misconfigured routes are identified.

Router-A

    admin@router-A> show configuration routing-instances
    VRF-A {
    instance-type vrf;`enter code here`
    vrf-target target:65001:100;
    routing-options {
        static {
            route 10.0.0.0/24 next-hop 1.2.3.4;
            route 10.0.1.0/24 next-hop 1.2.3.4;
            route 10.0.2.0/24 next-hop 1.2.3.4;
        }
    }


Router-B

    > admin@router-B> show configuration routing-instances
    VRF-A {
    instance-type vrf;`enter code here`
    vrf-target target:65001:100;
    routing-options {
        static {
            route 10.0.0.0/24 next-hop 1.2.3.4;
            route 10.0.2.0/24 next-hop 1.2.3.4;
        }
    }



**PrefixListCheck**

----------
This script is intended to be used for comparing the prefix-lists and their entries defined on two routers. Missing prefixes within an existing prefix-list as well as missing prefix-lists itself are identified.

Router-A

    > admin@Router-A> show configuration policy-options
    prefix-list TEST-A {
        10.20.30.0/24;
        10.20.31.0/24;
        10.20.32.0/24;
        10.20.33.0/24;
    }
    
Router-B

    > admin@Router-A> show configuration policy-options
    prefix-list TEST-A {
        10.20.30.0/24;
        10.20.32.0/24;
        10.20.33.0/24;
    }
    prefix-list TEST-B {
        10.20.30.0/24;
    }
    
    