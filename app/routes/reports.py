from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.routes.helpers import context
from app.services.report_queries import run_all_reports

router = APIRouter()


@router.get("/consultas", response_class=HTMLResponse)
def reports(request: Request, db: Session = Depends(get_db)) -> Response:
    """Muestra las veinte consultas de comprobación ejecutadas desde Python."""
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="reports/list.html",
        context=context(request, reports=run_all_reports(db)),
    )
