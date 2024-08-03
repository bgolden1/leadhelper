from utils.generator import generate_lead_allocation
from models.leads import Lead
from models.rep import SalesRep
from pprint import pprint

if __name__ == '__main__':
    rep1 = SalesRep('Rep1', '4301 Rosedale Ave, Austin, TX 78756', 3000)
    lead1 = Lead('812 Airport Blvd, Austin, TX 78702', 10)
    lead2 = Lead('11600 Menchaca Rd, Austin, TX 78748', 13)
    
    pprint(generate_lead_allocation([rep1], [lead1, lead2]))