from models.rep import SalesRep
from models.leads import Lead
import networkx as nx
import osmnx as ox


def generate_lead_allocation(reps: list[SalesRep], leads: list[Lead]):
    unallocated_leads = []
    ox.config(use_cache=True, log_console=True)

    place = 'Austin, TX, USA'
    G = ox.graph_from_place(place, network_type='drive')

    # impute missing edge speeds and add travel times
    G = ox.add_edge_speeds(G)
    G = ox.add_edge_travel_times(G)
    ordered_reps = sorted(reps, key=lambda x: x.vpi, reverse=True)
    ordered_leads = sorted(leads, key=lambda x: x.time)
    for lead in ordered_leads:
        for rep in ordered_reps:
            if rep.available and lead.time in rep.empty_timeslots:
                # check if rep has a previous lead and proximity to that or proximity to home if not
                if len(rep.allocated_leads) == 0:
                    # calculate time from home to lead
                    orig, dest = rep.home_location, lead.location
                    
                else:
                    # calculate time from previos lead to lead
                    orig, dest = rep.allocated_leads[-1].location, lead.location
                orig_node = ox.nearest_nodes(G, X=orig[1], Y=orig[0])
                dest_node = ox.nearest_nodes(G, X=dest[1], Y=dest[0])
                travel_time = nx.shortest_path_length(G, orig_node, dest_node, weight='travel_time')
                travel_time_nearest_min = round(travel_time / 60)
                if travel_time_nearest_min < 30:
                    rep.allocated_leads.append(lead)
                    rep.empty_timeslots.remove(lead.time)
                    lead.allocated = True
                    break
        if lead.allocated == False:
            unallocated_leads.append(lead)
            
    lead_allocation = {rep.name: [lead.address for lead in rep.allocated_leads] for rep in reps}
    lead_allocation['Unallocated Leads'] = [lead.address for lead in unallocated_leads]
    return lead_allocation
            