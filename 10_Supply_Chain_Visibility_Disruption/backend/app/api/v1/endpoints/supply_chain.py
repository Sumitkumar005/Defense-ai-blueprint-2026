from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, get_neo4j_driver
from app.models.supply_chain import Component

router = APIRouter()


@router.get("/components")
async def get_components(db: Session = Depends(get_db)):
    """Get all components"""
    components = db.query(Component).all()
    return {"components": components}


@router.get("/visibility/{component_id}")
async def get_supply_chain_visibility(
    component_id: int,
    db: Session = Depends(get_db)
):
    """Get multi-tier supply chain visibility using graph database"""
    
    # Query Neo4j for supply chain graph
    driver = get_neo4j_driver()
    
    with driver.session() as session:
        result = session.run("""
            MATCH path = (c:Component {id: $component_id})-[*1..5]-(s:Supplier)
            RETURN path
            LIMIT 100
        """, component_id=component_id)
        
        paths = [record["path"] for record in result]
    
    driver.close()
    
    return {
        "component_id": component_id,
        "supply_chain_tiers": len(paths),
        "graph_data": paths  # Would format properly in production
    }


