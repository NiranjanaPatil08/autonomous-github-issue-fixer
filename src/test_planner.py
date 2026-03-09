from src.agents.planner_agent import plan_issue


# Example GitHub issue
issue_title = "Fix crash when clicking 'Submit' button"
issue_body = """
The app crashes when the user clicks the Submit button on the contact form.
Steps to reproduce:
1. Open contact form
2. Fill in details
3. Click Submit
Observed: App crashes
Expected: Form should submit successfully without errors
"""

plan = plan_issue(issue_title, issue_body)
print("Planner Agent Output:")
print(plan)
