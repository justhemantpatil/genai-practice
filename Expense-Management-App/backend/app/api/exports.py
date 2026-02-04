from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db, get_current_user
from app.services.transaction_service import TransactionService
from app.models.user import User
import csv
import io

router = APIRouter()

@router.get("/transactions/csv")
async def export_transactions_csv(
    wallet_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    # Get all transactions (limit high or infinite)
    transactions = await service.get_transactions(wallet_id, current_user, skip=0, limit=100000)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Date", "Amount", "Type", "Category", "Description"])
    
    for txn in transactions:
        writer.writerow([
            txn.id,
            txn.date,
            txn.amount,
            txn.type,
            txn.category_id, # Should fetch category name ideally
            txn.description
        ])
    
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=transactions.csv"})
