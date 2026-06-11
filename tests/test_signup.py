from urllib.parse import quote

import pytest


pytestmark = pytest.mark.anyio


async def test_signup_adds_participant(client):
    activity = "Basketball Team"
    email = "student@mergington.edu"

    response = await client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    updated = (await client.get("/activities")).json()
    assert email in updated[activity]["participants"]


async def test_signup_rejects_duplicate_participant(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = await client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


async def test_signup_rejects_unknown_activity(client):
    response = await client.post("/activities/Unknown%20Club/signup?email=student%40mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


async def test_unregister_removes_participant(client):
    activity = "Basketball Team"
    email = "student@mergington.edu"

    signup_response = await client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    assert signup_response.status_code == 200

    response = await client.delete(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}

    updated = (await client.get("/activities")).json()
    assert email not in updated[activity]["participants"]


async def test_unregister_rejects_missing_participant(client):
    response = await client.delete("/activities/Chess%20Club/signup?email=missing%40mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


async def test_unregister_rejects_unknown_activity(client):
    response = await client.delete("/activities/Unknown%20Club/signup?email=student%40mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
