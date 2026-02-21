import uuid

from fastapi import APIRouter, HTTPException, status

from app.schemas import IssueCreate, IssueOut, IssueStatus, IssueUpdate
from app.security import CurrentUser
from app.storage import load_data, save_data

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])


@router.get("/", response_model=list[IssueOut])
def get_issues(current_user: CurrentUser) -> list[dict]:
    return load_data()


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
def create_issue(payload: IssueCreate, current_user: CurrentUser) -> IssueOut:
    issues = load_data()
    new_issue = IssueOut(
        id=str(uuid.uuid4()),
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status=IssueStatus.OPEN,
    )
    issues.append(new_issue.model_dump())
    save_data(issues)
    return new_issue


@router.get("/{issue_id}", response_model=IssueOut)
def get_issue(issue_id: str, current_user: CurrentUser) -> dict:
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            return issue
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
    )


@router.put("/{issue_id}", response_model=IssueOut)
def update_issue(
    issue_id: str, payload: IssueUpdate, current_user: CurrentUser
) -> dict:
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            issue.update(payload.model_dump(exclude_unset=True))
            save_data(issues)
            return issue
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
    )


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_issue(issue_id: str, current_user: CurrentUser) -> None:
    issues = load_data()
    for issue in issues:
        if issue["id"] == issue_id:
            issues.remove(issue)
            save_data(issues)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Issue not found"
    )
