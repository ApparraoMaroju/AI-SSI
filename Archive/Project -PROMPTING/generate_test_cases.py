"""
Generate VWO A/B Testing Platform – Comprehensive Test Cases XLSX
Template Reference : FTC02-PRD to Test Cases (Comprehensive)
Author            : Apparao Maroju
Date              : March 31, 2026
"""
import subprocess, sys

try:
    import openpyxl
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    import openpyxl

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUTPUT_PATH = r"c:\Apparao Maroju\AI-SSI\Project -PROMPTING\Output\VWO-AB-Testing-TestCases.xlsx"

# ── Styling constants ───────────────────────────────────────────────────────
HEADER_FILL   = PatternFill("solid", fgColor="1F3864")
ALT_FILL      = PatternFill("solid", fgColor="EBF1FA")
WHITE_FILL    = PatternFill("solid", fgColor="FFFFFF")
HEADER_FONT   = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
BODY_FONT     = Font(name="Calibri", size=10)
BOLD_FONT     = Font(name="Calibri", bold=True, size=10)
C_ALIGN       = Alignment(horizontal="center", vertical="top",   wrap_text=True)
L_ALIGN       = Alignment(horizontal="left",   vertical="top",   wrap_text=True)

THIN = Border(
    left  =Side(style="thin", color="BFBFBF"),
    right =Side(style="thin", color="BFBFBF"),
    top   =Side(style="thin", color="BFBFBF"),
    bottom=Side(style="thin", color="BFBFBF"),
)

PRIO_COLOR = {"High": "C00000", "Medium": "ED7D31", "Low": "70AD47"}
STATUS_COLOR = {
    "Pass":   "375623",
    "Fail":   "C00000",
    "Blocked":"7030A0",
    "N/A":    "595959",
    "":       "595959",
}
CAT_COLOR = {
    "Authentication":          "2E4DA0",
    "Remember Me":             "4472C4",
    "Session Management":      "2E75B6",
    "Multi-Factor Auth (2FA)": "833C00",
    "Single Sign-On (SSO)":    "375623",
    "Input Validation":        "7030A0",
    "Password Management":     "C55A11",
    "Security":                "C00000",
    "Performance":             "006B6B",
    "Accessibility":           "1F6864",
    "UI / UX":                 "4472C4",
    "Integration":             "2E4DA0",
    "End-to-End Flow":         "1F3864",
}

# ── Test Case Data ──────────────────────────────────────────────────────────
# TID | Category | Description | Pre-conditions | Steps | Expected Result | Priority
TESTCASES = [

    # ── AUTHENTICATION ──────────────────────────────────────────────────────
    (
        "TC-AUTH-001", "Authentication",
        "Login with valid registered email and correct password",
        "1. User has a registered VWO account\n2. App.vwo.com is accessible\n3. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter valid registered email address\n3. Enter correct password\n4. Click the 'Login' button",
        "1. User is authenticated successfully\n2. User is redirected to the VWO dashboard\n3. Dashboard loads within 3 seconds\n4. User's name/account context is displayed",
        "High"
    ),
    (
        "TC-AUTH-002", "Authentication",
        "Login with valid email but incorrect password",
        "1. User has a registered VWO account\n2. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter valid registered email address\n3. Enter an incorrect password\n4. Click the 'Login' button",
        "1. Login is rejected\n2. A clear, actionable error message is displayed\n3. User remains on the login page\n4. Password field is cleared",
        "High"
    ),
    (
        "TC-AUTH-003", "Authentication",
        "Login with a non-existent / unregistered email address",
        "1. User is on the login page\n2. The email address being used is NOT registered",
        "1. Navigate to https://app.vwo.com\n2. Enter an email address not registered with VWO\n3. Enter any password\n4. Click the 'Login' button",
        "1. Login is rejected\n2. An appropriate error message is displayed\n3. User remains on the login page",
        "High"
    ),
    (
        "TC-AUTH-004", "Authentication",
        "Login attempt with email field left empty",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Leave the email field empty\n3. Enter any value in the password field\n4. Click the 'Login' button",
        "1. Form submission is prevented\n2. Inline validation error message is shown for the email field\n3. User remains on the login page",
        "High"
    ),
    (
        "TC-AUTH-005", "Authentication",
        "Login attempt with password field left empty",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter a valid email address\n3. Leave the password field empty\n4. Click the 'Login' button",
        "1. Form submission is prevented\n2. Inline validation error message is shown for the password field\n3. User remains on the login page",
        "High"
    ),
    (
        "TC-AUTH-006", "Authentication",
        "Login attempt with both email and password fields empty",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Leave both email and password fields empty\n3. Click the 'Login' button",
        "1. Form submission is prevented\n2. Validation error messages appear for both fields\n3. User remains on the login page",
        "High"
    ),
    (
        "TC-AUTH-007", "Authentication",
        "Login with invalid email format (missing @ symbol)",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter 'userwithoutatsign.com' in the email field\n3. Enter any password\n4. Click the 'Login' button or tab out of email field",
        "1. Real-time validation triggers on blur\n2. Email format error message is displayed inline\n3. Form submission is prevented",
        "Medium"
    ),
    (
        "TC-AUTH-008", "Authentication",
        "Login with invalid email format (missing domain extension)",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter 'user@nodomain' in the email field\n3. Enter any password\n4. Tab out of email field",
        "1. Real-time validation triggers on blur\n2. Email format error message is displayed inline",
        "Medium"
    ),
    (
        "TC-AUTH-009", "Authentication",
        "Login email field is case-insensitive",
        "1. User has a registered account with email 'User@Example.com'\n2. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter 'user@example.com' in lowercase in the email field\n3. Enter the correct password\n4. Click the 'Login' button",
        "1. Login is successful\n2. User is redirected to the dashboard\n3. Email comparison is case-insensitive",
        "Medium"
    ),
    (
        "TC-AUTH-010", "Authentication",
        "Login fails when email contains leading or trailing whitespace only",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter '  user@example.com  ' (with spaces) in email field\n3. Enter any password\n4. Click 'Login'",
        "1. System either trims whitespace and processes login OR displays a validation error\n2. Behavior is consistent and predictable\n3. No system crash or unhandled exception",
        "Low"
    ),
    (
        "TC-AUTH-011", "Authentication",
        "Login with copied/pasted credentials from clipboard",
        "1. User has valid credentials\n2. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Copy a valid email from clipboard and paste into email field\n3. Copy a valid password from clipboard and paste into password field\n4. Click 'Login'",
        "1. Pasted values are accepted in both fields\n2. Login is successful\n3. Password is masked even when pasted",
        "Low"
    ),

    # ── REMEMBER ME ─────────────────────────────────────────────────────────
    (
        "TC-REM-001", "Remember Me",
        "Remember Me checked – session persists after browser close and reopen",
        "1. User has a registered account\n2. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter valid email and password\n3. Check the 'Remember Me' checkbox\n4. Click 'Login'\n5. Close the browser completely\n6. Reopen the browser and navigate to app.vwo.com",
        "1. User is still logged in without needing to re-enter credentials\n2. Dashboard is accessible directly",
        "Medium"
    ),
    (
        "TC-REM-002", "Remember Me",
        "Remember Me unchecked – session is NOT persisted after browser close",
        "1. User has a registered account\n2. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter valid email and password\n3. Ensure 'Remember Me' checkbox is unchecked\n4. Click 'Login'\n5. Close the browser completely\n6. Reopen the browser and navigate to app.vwo.com",
        "1. User is redirected to the login page\n2. Credentials are not pre-filled\n3. User must log in again",
        "Medium"
    ),
    (
        "TC-REM-003", "Remember Me",
        "Remember Me checkbox default state is unchecked on fresh page load",
        "1. User navigates to login page for the first time or in incognito mode",
        "1. Navigate to https://app.vwo.com in a fresh/incognito browser session",
        "1. The 'Remember Me' checkbox is unchecked by default\n2. No pre-filled credentials are present",
        "Low"
    ),

    # ── SESSION MANAGEMENT ──────────────────────────────────────────────────
    (
        "TC-SESS-001", "Session Management",
        "User session expires after the configured inactivity timeout period",
        "1. User is logged in to VWO\n2. Session timeout period is configured (e.g., 30 minutes)",
        "1. Log in to app.vwo.com successfully\n2. Leave the application idle for the duration exceeding the configured session timeout\n3. Attempt to interact with the page or navigate",
        "1. Session expires after the configured inactivity period\n2. User is automatically redirected to the login page\n3. A session expiry message is displayed",
        "High"
    ),
    (
        "TC-SESS-002", "Session Management",
        "User is redirected to login page upon session expiry",
        "1. User is logged in\n2. Session has expired (inactivity timeout reached)",
        "1. Allow active session to expire\n2. Attempt to click any menu item or navigate to an authenticated page",
        "1. User is redirected to the login page\n2. A clear session expiry notification is shown",
        "High"
    ),
    (
        "TC-SESS-003", "Session Management",
        "Session token is invalidated immediately after user logs out",
        "1. User is logged in to VWO",
        "1. Log in to app.vwo.com\n2. Copy the session token/cookie value from browser dev tools\n3. Click 'Logout'\n4. Attempt to use the copied session token to access an authenticated page",
        "1. Logout is successful\n2. The old session token is invalid\n3. Attempt to access authenticated pages with old token is rejected\n4. User is redirected to login page",
        "High"
    ),
    (
        "TC-SESS-004", "Session Management",
        "Back button does not allow access to authenticated pages after logout",
        "1. User is logged in to VWO",
        "1. Log in to app.vwo.com\n2. Navigate to the dashboard\n3. Click 'Logout'\n4. Press the browser's Back button",
        "1. Browser does not display cached authenticated content\n2. User is redirected to the login page\n3. No authenticated data is exposed",
        "High"
    ),
    (
        "TC-SESS-005", "Session Management",
        "Concurrent session handling – same user logs in from two different browsers",
        "1. User has a registered account",
        "1. Log in to app.vwo.com in Browser A\n2. Log in to app.vwo.com in Browser B with the same credentials\n3. Perform actions in both sessions",
        "1. Both sessions are handled per the system's concurrent session policy\n2. No unhandled errors or crashes\n3. Behavior is as per PRD specification (concurrent session policy noted as Needs Clarification)",
        "Medium"
    ),

    # ── MULTI-FACTOR AUTHENTICATION (2FA) ───────────────────────────────────
    (
        "TC-2FA-001", "Multi-Factor Auth (2FA)",
        "User can enable 2FA from account security settings",
        "1. User is logged in to VWO\n2. 2FA is currently disabled",
        "1. Log in to app.vwo.com\n2. Navigate to Account Settings > Security\n3. Click 'Enable Two-Factor Authentication'\n4. Follow the setup wizard (scan QR code or enter key)\n5. Enter the generated 6-digit code to confirm",
        "1. 2FA is enabled successfully\n2. Confirmation message is displayed\n3. Subsequent logins prompt for a 2FA code",
        "High"
    ),
    (
        "TC-2FA-002", "Multi-Factor Auth (2FA)",
        "Successful login using valid 2FA verification code",
        "1. User has a registered account with 2FA enabled\n2. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter valid email and password\n3. Click 'Login'\n4. When prompted, enter the current valid 6-digit 2FA code\n5. Click 'Verify'",
        "1. 2FA code is accepted\n2. User is redirected to the VWO dashboard\n3. Login is complete",
        "High"
    ),
    (
        "TC-2FA-003", "Multi-Factor Auth (2FA)",
        "Login rejected with an invalid/incorrect 2FA code",
        "1. User has 2FA enabled\n2. User has passed email/password step and is at 2FA prompt",
        "1. At the 2FA prompt, enter an invalid 6-digit code (e.g., '000000')\n2. Click 'Verify'",
        "1. 2FA verification is rejected\n2. Clear error message is displayed\n3. User remains on the 2FA verification screen\n4. Email/password auth is NOT rolled back",
        "High"
    ),
    (
        "TC-2FA-004", "Multi-Factor Auth (2FA)",
        "Login rejected with an expired 2FA code (boundary – code age > 30 seconds)",
        "1. User has 2FA enabled\n2. User is at the 2FA verification prompt",
        "1. Wait until a 2FA code is about to expire (past the TOTP validity window)\n2. Enter the expired code\n3. Click 'Verify'",
        "1. Expired 2FA code is rejected\n2. Clear error message stating the code has expired is shown\n3. User is prompted to enter a new code",
        "High"
    ),
    (
        "TC-2FA-005", "Multi-Factor Auth (2FA)",
        "Resend / regenerate 2FA code functionality",
        "1. User has 2FA enabled\n2. User is at the 2FA verification prompt",
        "1. At the 2FA prompt, click 'Resend Code' or 'Get a new code'\n2. Receive new code via the configured method\n3. Enter the new code and click 'Verify'",
        "1. New 2FA code is sent/generated successfully\n2. Old code is invalidated once new code is issued\n3. New valid code allows successful login",
        "Medium"
    ),

    # ── SINGLE SIGN-ON (SSO) ────────────────────────────────────────────────
    (
        "TC-SSO-001", "Single Sign-On (SSO)",
        "Successful enterprise login via SAML SSO provider",
        "1. Enterprise SSO (SAML) is configured for the organisation\n2. User has a valid enterprise account",
        "1. Navigate to https://app.vwo.com\n2. Click 'Sign in with SSO' or enter the enterprise email\n3. Select SAML provider\n4. Complete authentication on the identity provider's page\n5. Return to VWO",
        "1. SAML authentication completes successfully\n2. User is redirected to the VWO dashboard\n3. User is logged in with correct role/permissions",
        "High"
    ),
    (
        "TC-SSO-002", "Single Sign-On (SSO)",
        "Successful enterprise login via OAuth 2.0 SSO provider",
        "1. Enterprise SSO (OAuth 2.0) is configured\n2. User has valid enterprise OAuth credentials",
        "1. Navigate to https://app.vwo.com\n2. Click 'Sign in with SSO'\n3. Select OAuth provider\n4. Complete OAuth authorization flow\n5. Return to VWO",
        "1. OAuth authentication completes successfully\n2. User is redirected to the VWO dashboard\n3. Correct permissions are assigned",
        "High"
    ),
    (
        "TC-SSO-003", "Single Sign-On (SSO)",
        "SSO login fails gracefully with an invalid or tampered SSO token",
        "1. SAML/OAuth SSO is configured",
        "1. Navigate to https://app.vwo.com\n2. Initiate SSO login flow\n3. Intercept and tamper with the SAML assertion/OAuth token\n4. Submit the tampered response to VWO",
        "1. SSO authentication is rejected\n2. Clear error message is displayed\n3. User is NOT logged in\n4. System logs the failed SSO attempt",
        "High"
    ),
    (
        "TC-SSO-004", "Single Sign-On (SSO)",
        "SSO login via Google identity provider",
        "1. Google SSO integration is enabled\n2. User has a valid Google account linked to VWO",
        "1. Navigate to https://app.vwo.com\n2. Click 'Sign in with Google'\n3. Complete Google OAuth authentication\n4. Return to VWO",
        "1. Google OAuth flow completes\n2. User is logged in to VWO\n3. Dashboard is displayed",
        "Medium"
    ),
    (
        "TC-SSO-005", "Single Sign-On (SSO)",
        "SSO login via Microsoft identity provider",
        "1. Microsoft SSO integration is enabled\n2. User has a valid Microsoft account linked to VWO",
        "1. Navigate to https://app.vwo.com\n2. Click 'Sign in with Microsoft'\n3. Complete Microsoft OAuth authentication\n4. Return to VWO",
        "1. Microsoft OAuth flow completes\n2. User is logged in to VWO\n3. Dashboard is displayed",
        "Medium"
    ),
    (
        "TC-SSO-006", "Single Sign-On (SSO)",
        "Error message displayed when SSO identity provider is unreachable",
        "1. SAML/OAuth SSO is configured\n2. The identity provider is simulated as unavailable",
        "1. Navigate to https://app.vwo.com\n2. Initiate SSO login\n3. Identity provider returns an error or is unreachable",
        "1. VWO displays a user-friendly error message\n2. User is NOT redirected to dashboard\n3. Option to try again or use email/password login is available",
        "Medium"
    ),

    # ── INPUT VALIDATION ────────────────────────────────────────────────────
    (
        "TC-VAL-001", "Input Validation",
        "Real-time email validation triggers on field blur",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Click on the email field\n3. Enter an invalid email (e.g., 'invalidemail')\n4. Click or Tab out of the email field (blur event)",
        "1. Validation fires on blur (not on each keystroke)\n2. Inline error message appears below the email field\n3. No full-page refresh occurs",
        "Medium"
    ),
    (
        "TC-VAL-002", "Input Validation",
        "Email field validates and rejects address without @ symbol",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter 'testexample.com' in the email field\n3. Tab out of the field",
        "1. Real-time validation shows error\n2. Error message clearly states invalid email format",
        "Medium"
    ),
    (
        "TC-VAL-003", "Input Validation",
        "Email field validates and rejects address without domain extension",
        "1. User is on the login page",
        "1. Enter 'test@nodomain' in the email field\n2. Tab out of the field",
        "1. Validation error is shown\n2. Error message reflects invalid format",
        "Medium"
    ),
    (
        "TC-VAL-004", "Input Validation",
        "Password field masks characters by default",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Click on the password field\n3. Type any characters",
        "1. All typed characters appear as bullet points or asterisks\n2. Password text is NOT visible in plain text",
        "High"
    ),
    (
        "TC-VAL-005", "Input Validation",
        "Password strength indicator updates dynamically as password is typed",
        "1. User is on a page with a password strength indicator (registration or reset page)",
        "1. Navigate to a password input page\n2. Type a weak password (e.g., '123')\n3. Observe the strength indicator\n4. Type a stronger password (mix of upper, lower, numbers, symbols)\n5. Observe the strength indicator",
        "1. Strength indicator updates in real-time\n2. Weak passwords display low/red indicator\n3. Strong passwords display high/green indicator",
        "Medium"
    ),
    (
        "TC-VAL-006", "Input Validation",
        "Email field enforces maximum character length (boundary)",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter an email address longer than the system maximum (e.g., 256+ characters)\n3. Attempt to submit",
        "1. Email field either prevents entry beyond max length OR shows a validation error\n2. System does not crash or throw an unhandled error",
        "Medium"
    ),
    (
        "TC-VAL-007", "Input Validation",
        "Password field enforces minimum length requirement (boundary – below minimum)",
        "1. User is on the login or registration page",
        "1. Enter a password shorter than the minimum required length (e.g., 1 character)\n2. Tab out of the field or submit the form",
        "1. Validation error is shown indicating the minimum password length requirement\n2. Form submission is prevented",
        "Medium"
    ),
    (
        "TC-VAL-008", "Input Validation",
        "Password field accepts input at exactly the minimum allowed length (boundary – at minimum)",
        "1. User is on a password input page\n2. Minimum length requirement is known",
        "1. Enter a password of exactly the minimum required length\n2. Attempt to proceed",
        "1. Password is accepted as valid at the boundary value\n2. No error message is shown for length",
        "Medium"
    ),
    (
        "TC-VAL-009", "Input Validation",
        "Clickable form labels focus the corresponding input field",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Click on the text label 'Email' (not the input field)\n3. Click on the text label 'Password' (not the input field)",
        "1. Clicking 'Email' label focuses the email input field\n2. Clicking 'Password' label focuses the password input field\n3. Keyboard cursor is active in the focused field",
        "Low"
    ),
    (
        "TC-VAL-010", "Input Validation",
        "Auto-focus is applied to the first field (email) on page load",
        "1. User navigates to https://app.vwo.com login page",
        "1. Navigate to https://app.vwo.com\n2. Observe which field has focus when the page finishes loading",
        "1. The email input field has keyboard focus automatically\n2. User can begin typing their email without clicking the field\n3. Focus indicator is visible on the email field",
        "Medium"
    ),

    # ── PASSWORD MANAGEMENT ─────────────────────────────────────────────────
    (
        "TC-PWD-001", "Password Management",
        "'Forgot Password' link is visible and navigates to the password reset page",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Locate the 'Forgot Password' or 'Forgot your password?' link\n3. Click the link",
        "1. A 'Forgot Password' link is visible on the login page\n2. Clicking the link navigates to the password reset/recovery page\n3. User is NOT logged in by this action",
        "High"
    ),
    (
        "TC-PWD-002", "Password Management",
        "Password reset email is sent to the registered email address",
        "1. User has a registered VWO account\n2. User is on the Forgot Password page",
        "1. Navigate to the Forgot Password page\n2. Enter the registered email address\n3. Click 'Send Reset Link' or equivalent",
        "1. Confirmation message is displayed (e.g., 'Check your email for a reset link')\n2. A password reset email is received at the provided address\n3. Email contains a secure reset link",
        "High"
    ),
    (
        "TC-PWD-003", "Password Management",
        "Password reset with a valid and unexpired reset token is successful",
        "1. User has initiated a password reset and received the reset email\n2. Reset token is valid and within expiry period",
        "1. Open the password reset email\n2. Click the reset link\n3. Enter a new password that meets complexity requirements\n4. Confirm the new password\n5. Click 'Reset Password'",
        "1. Password is reset successfully\n2. Confirmation message is displayed\n3. User is redirected to the login page\n4. Old password is invalidated",
        "High"
    ),
    (
        "TC-PWD-004", "Password Management",
        "Password reset fails with an expired reset token (boundary – past token validity)",
        "1. User has a password reset email\n2. The reset token has expired",
        "1. Wait until the reset token expires\n2. Click the reset link from the email\n3. Attempt to set a new password",
        "1. System detects expired token\n2. Clear error message stating 'The reset link has expired'\n3. Option to request a new reset link is provided\n4. Password is NOT changed",
        "High"
    ),
    (
        "TC-PWD-005", "Password Management",
        "Password reset token cannot be reused after a successful reset",
        "1. User has performed a successful password reset using a valid token",
        "1. Complete a successful password reset using a valid reset link\n2. Go back and click the same reset link again\n3. Attempt to set another password using the same token",
        "1. System rejects the already-used token\n2. Error message indicates the link is invalid or has already been used\n3. Password is NOT changed a second time with the old token",
        "High"
    ),
    (
        "TC-PWD-006", "Password Management",
        "New password must meet defined complexity requirements",
        "1. User is on the password reset page with a valid token",
        "1. Enter a new password that intentionally fails complexity rules (e.g., '12345' – too short, too simple)\n2. Click 'Reset Password'",
        "1. Password is rejected\n2. Error message clearly describes the complexity requirements\n3. Password is NOT saved",
        "High"
    ),
    (
        "TC-PWD-007", "Password Management",
        "User is redirected to login page after a successful password reset",
        "1. User has completed a successful password reset",
        "1. Complete the password reset flow with a valid token and valid new password\n2. Click 'Reset Password'\n3. Observe the redirect",
        "1. Password is reset successfully\n2. User is redirected to the login page\n3. Success message is shown",
        "Medium"
    ),
    (
        "TC-PWD-008", "Password Management",
        "Password reset fails when 'new password' and 'confirm password' do not match",
        "1. User is on the password reset page with a valid token",
        "1. Enter a new password in the 'New Password' field\n2. Enter a different value in the 'Confirm Password' field\n3. Click 'Reset Password'",
        "1. Password reset is rejected\n2. Clear error message shown: passwords do not match\n3. Password is NOT changed",
        "High"
    ),
    (
        "TC-PWD-009", "Password Management",
        "Forgot password flow with an unregistered email shows a safe response",
        "1. User is on the Forgot Password page",
        "1. Enter an email address that is NOT registered with VWO\n2. Click 'Send Reset Link'",
        "1. System displays the same confirmation message as for valid emails (prevents email enumeration)\n2. No real reset email is sent\n3. System does not reveal whether the email is registered or not",
        "High"
    ),

    # ── SECURITY ────────────────────────────────────────────────────────────
    (
        "TC-SEC-001", "Security",
        "Account is locked out after N consecutive failed login attempts (brute force protection)",
        "1. User has a registered account\n2. Rate limiting / lockout is configured",
        "1. Navigate to https://app.vwo.com\n2. Enter the correct email address\n3. Enter an incorrect password repeatedly (exceed the allowed attempt threshold)\n4. Observe system behaviour",
        "1. After exceeding the failed attempt threshold, the account is temporarily locked\n2. Lockout message is displayed to the user\n3. Successful attempts are blocked during the lockout period\n4. Lockout event is logged",
        "High"
    ),
    (
        "TC-SEC-002", "Security",
        "Rate limiting is enforced on the login API endpoint",
        "1. Access to the login API endpoint",
        "1. Send a high volume of POST requests to the login API endpoint in rapid succession\n2. Observe HTTP response codes",
        "1. After exceeding the rate limit, the API returns HTTP 429 (Too Many Requests)\n2. Requests beyond the limit are throttled\n3. Legitimate users can retry after the throttle window",
        "High"
    ),
    (
        "TC-SEC-003", "Security",
        "SQL injection in the email field does not compromise the system",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter a SQL injection string in the email field (e.g.: ' OR '1'='1'; --)\n3. Enter any password\n4. Click 'Login'",
        "1. Login is rejected\n2. No database error messages are exposed to the user\n3. System remains stable and does not expose data\n4. Input is sanitized / parameterized",
        "High"
    ),
    (
        "TC-SEC-004", "Security",
        "SQL injection in the password field does not compromise the system",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter a valid registered email\n3. Enter a SQL injection payload in the password field (e.g.: ' OR '1'='1')\n4. Click 'Login'",
        "1. Login is rejected\n2. No database errors are exposed\n3. System is not compromised",
        "High"
    ),
    (
        "TC-SEC-005", "Security",
        "XSS (Cross-Site Scripting) injection in login form fields is sanitized",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter a script injection string in the email field (e.g.: <script>alert('XSS')</script>)\n3. Enter a script payload in the password field\n4. Click 'Login'",
        "1. No script is executed in the browser\n2. Input is sanitized or escaped\n3. No alert dialog or script side-effects are observed\n4. Error message is displayed normally",
        "High"
    ),
    (
        "TC-SEC-006", "Security",
        "CSRF token is present and validated on login form submission",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Inspect the login form source for a CSRF token field\n3. Attempt to submit the form with a missing or tampered CSRF token using browser dev tools",
        "1. A CSRF token is present as a hidden field in the login form\n2. Submission with missing/invalid CSRF token is rejected\n3. Appropriate error is returned (403 Forbidden or equivalent)",
        "High"
    ),
    (
        "TC-SEC-007", "Security",
        "HTTP requests are automatically redirected to HTTPS (SSL/TLS enforcement)",
        "1. User has access to http:// version of the URL",
        "1. Type 'http://app.vwo.com' in the browser address bar\n2. Press Enter\n3. Observe the redirect",
        "1. Browser is automatically redirected from HTTP to HTTPS\n2. Page loads over HTTPS with a valid SSL certificate\n3. Browser shows a secure padlock icon",
        "High"
    ),
    (
        "TC-SEC-008", "Security",
        "Password is NOT visible in page source, network logs, or browser console",
        "1. User is on the login page\n2. Browser DevTools are open",
        "1. Navigate to https://app.vwo.com\n2. Open browser Developer Tools (Network tab)\n3. Enter valid email and password\n4. Click 'Login'\n5. Inspect the network request payload and browser console logs",
        "1. Password field value is not visible in the page HTML source\n2. Password is not logged in browser Console\n3. If submitted over HTTPS, plain-text password is not visible in network interceptors",
        "High"
    ),
    (
        "TC-SEC-009", "Security",
        "Credentials are not exposed in URL query parameters",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter valid credentials\n3. Click 'Login'\n4. Observe the URL in the browser address bar during and after login",
        "1. Email and password are not appended to the URL as query parameters\n2. URL remains clean (no sensitive data in GET parameters)",
        "High"
    ),
    (
        "TC-SEC-010", "Security",
        "Session token is not exposed in URL parameters",
        "1. User is logged in to VWO",
        "1. Log in to app.vwo.com\n2. Observe all URLs navigated to post-login in the browser address bar\n3. Inspect network requests for session token in URL parameters",
        "1. Session tokens / authentication tokens are never appended to URL query strings\n2. Tokens are transmitted via cookies or Authorization headers only",
        "High"
    ),
    (
        "TC-SEC-011", "Security",
        "GDPR compliance – login page does not collect unnecessary personal data",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Inspect cookies set by the login page before login\n3. Inspect network requests for any unnecessary data collection",
        "1. Only necessary cookies are set\n2. No unnecessary personal data is collected without user consent\n3. Privacy policy link is accessible from the login page",
        "Medium"
    ),

    # ── PERFORMANCE ─────────────────────────────────────────────────────────
    (
        "TC-PERF-001", "Performance",
        "Login page loads within 2 seconds on a standard network connection (20 Mbps)",
        "1. Test machine is on a standard Wi-Fi connection (~20 Mbps)\n2. Browser DevTools is open (Network tab)",
        "1. Open a new browser tab\n2. Clear browser cache\n3. Navigate to https://app.vwo.com\n4. Record the page load time from browser DevTools or Lighthouse",
        "1. Login page fully loads in under 2 seconds\n2. All critical assets (CSS, JS, fonts) are loaded\n3. No blocking resources observed",
        "High"
    ),
    (
        "TC-PERF-002", "Performance",
        "Login page load time on a simulated slow/3G network (1.5 Mbps)",
        "1. Browser DevTools is available\n2. Network throttling can be configured",
        "1. Open browser DevTools > Network tab\n2. Enable 3G throttling (1.5 Mbps)\n3. Navigate to https://app.vwo.com\n4. Record the page load time",
        "1. Login page eventually loads on slow network\n2. Page is functional (all form elements render)\n3. Load time is recorded for benchmarking; acceptable degradation is expected\n4. No crashes or blank page",
        "Medium"
    ),
    (
        "TC-PERF-003", "Performance",
        "VWO dashboard loads within 3 seconds after successful authentication",
        "1. User has valid credentials\n2. Standard network connection",
        "1. Navigate to https://app.vwo.com\n2. Log in with valid credentials\n3. Measure the time from clicking 'Login' to full dashboard render",
        "1. Dashboard fully loads within 3 seconds after login\n2. Navigation menu and content panels are visible\n3. No visible loading errors",
        "High"
    ),
    (
        "TC-PERF-004", "Performance",
        "Platform availability meets 99.9% uptime SLA target",
        "1. Uptime monitoring tool is configured (e.g., UptimeRobot, Pingdom)\n2. Monitoring period is at least 30 days",
        "1. Configure uptime monitoring on https://app.vwo.com\n2. Run monitoring over a 30-day period\n3. Review uptime report at the end of the period",
        "1. Uptime is at or above 99.9% during the monitoring period\n2. No unplanned outages exceed the allowable downtime (~43.8 minutes/month)",
        "High"
    ),
    (
        "TC-PERF-005", "Performance",
        "System handles concurrent login requests from multiple users simultaneously",
        "1. Load testing tool is configured (JMeter or k6)\n2. Test user accounts are prepared",
        "1. Configure a load test scenario simulating 100 concurrent users\n2. Each virtual user performs: navigate to login page → enter credentials → submit login\n3. Run the load test and observe response times and error rates",
        "1. All 100 concurrent login requests are processed\n2. Average login response time remains within acceptable thresholds\n3. Error rate is below acceptable limits\n4. No system crash or timeout errors",
        "Medium"
    ),

    # ── ACCESSIBILITY ────────────────────────────────────────────────────────
    (
        "TC-A11Y-001", "Accessibility",
        "Full keyboard navigation through the login form using Tab, Enter, and Escape",
        "1. User is on the login page\n2. User will not use mouse",
        "1. Navigate to https://app.vwo.com\n2. Press Tab to move from the auto-focused email field\n3. Tab through each interactive element (email → password → Remember Me → Login button → Forgot Password)\n4. Press Enter on the Login button\n5. Press Escape if any modal/dialog is triggered",
        "1. Tab order is logical and sequential\n2. All interactive elements are reachable via keyboard\n3. Enter key submits the form when Login button is focused\n4. Escape dismisses modals if applicable\n5. No keyboard traps are encountered",
        "High"
    ),
    (
        "TC-A11Y-002", "Accessibility",
        "Screen reader correctly announces all form labels, inputs, and error messages (ARIA)",
        "1. Screen reader (NVDA or JAWS) is installed and active\n2. User is on the login page",
        "1. Activate NVDA/JAWS screen reader\n2. Navigate to https://app.vwo.com\n3. Navigate through all form elements using keyboard\n4. Intentionally submit the form with empty fields\n5. Listen to how error messages are announced",
        "1. Screen reader announces each form label when input is focused\n2. All ARIA labels and roles are correctly implemented\n3. Error messages are announced immediately when they appear\n4. No unlabeled interactive elements",
        "High"
    ),
    (
        "TC-A11Y-003", "Accessibility",
        "Color contrast ratio for all text elements is at minimum 4.5:1 (WCAG 2.1 AA)",
        "1. Browser with Axe DevTools or Lighthouse installed",
        "1. Navigate to https://app.vwo.com\n2. Open Axe DevTools extension\n3. Run accessibility audit\n4. Review color contrast failures specific to the login page",
        "1. All text elements pass the 4.5:1 minimum contrast ratio\n2. No color contrast violations are reported by Axe\n3. Both Light and Dark Mode themes pass the test",
        "Medium"
    ),
    (
        "TC-A11Y-004", "Accessibility",
        "Auto-focus is set on the email input field when the login page loads",
        "1. User is navigating to the login page",
        "1. Navigate to https://app.vwo.com\n2. Observe which element has keyboard focus when the page finishes loading\n3. Start typing immediately without clicking",
        "1. Email input field has keyboard focus on page load\n2. Typed characters appear in the email field\n3. No click required to begin entering credentials",
        "Medium"
    ),
    (
        "TC-A11Y-005", "Accessibility",
        "High Contrast Mode renders all elements legibly",
        "1. User is on the login page",
        "1. Enable Windows High Contrast Mode (Settings > Ease of Access > High Contrast)\n2. Navigate to https://app.vwo.com\n3. Inspect all login page elements",
        "1. All text, form elements, and buttons are legible in High Contrast Mode\n2. No elements are invisible or unreadable\n3. Interactive elements remain functional",
        "Medium"
    ),
    (
        "TC-A11Y-006", "Accessibility",
        "Inline error messages are programmatically associated with their form fields via ARIA",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Submit the form with empty fields\n3. Inspect the error message elements in browser DevTools\n4. Check for aria-describedby or aria-live attributes",
        "1. Each error message is linked to its corresponding input via aria-describedby\n2. aria-live region or role='alert' is used so screen readers announce errors automatically\n3. Screen reader announces errors without user needing to navigate to them",
        "High"
    ),
    (
        "TC-A11Y-007", "Accessibility",
        "Focus indicators are visible on all interactive elements during keyboard navigation",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Press Tab to navigate through all interactive elements\n3. Observe the focus highlight/outline on each element",
        "1. A visible focus indicator (outline/ring) is present on every focused element\n2. Focus indicator is distinguishable against the page background (passes contrast)\n3. No element has outline:none without an alternative visible indicator",
        "Medium"
    ),

    # ── UI / UX ──────────────────────────────────────────────────────────────
    (
        "TC-UI-001", "UI / UX",
        "Light Mode theme displays correctly across all login page elements",
        "1. User is on the login page\n2. Light Mode is selected or is the default",
        "1. Navigate to https://app.vwo.com\n2. Select Light Mode (or confirm it is default)\n3. Inspect the page visually for correct rendering",
        "1. Background, text, form fields, and buttons all display with light theme colors\n2. VWO branding is consistent with design guidelines\n3. All elements are readable and correctly positioned",
        "Medium"
    ),
    (
        "TC-UI-002", "UI / UX",
        "Dark Mode theme displays correctly across all login page elements",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Toggle to Dark Mode using the provided UI option\n3. Inspect the page visually for correct rendering",
        "1. Background, text, form fields, and buttons switch to dark theme colors\n2. All text remains readable with sufficient contrast\n3. VWO logo and branding adapt to dark theme",
        "Medium"
    ),
    (
        "TC-UI-003", "UI / UX",
        "Login page is fully responsive on mobile devices (smartphone – 375×667)",
        "1. Test on a smartphone or use browser DevTools device emulation",
        "1. Open browser DevTools\n2. Switch to mobile emulation (e.g., iPhone SE – 375×667)\n3. Navigate to https://app.vwo.com\n4. Test interaction with all login form elements",
        "1. Login form is fully visible without horizontal scroll\n2. Form elements are touch-friendly (adequate tap target sizes)\n3. Virtual keyboard does not obscure the active input field\n4. All functionality works on mobile",
        "Medium"
    ),
    (
        "TC-UI-004", "UI / UX",
        "Login page is fully responsive on tablet devices (768×1024)",
        "1. Test on a tablet or browser DevTools tablet emulation",
        "1. Open browser DevTools\n2. Switch to tablet emulation (e.g., iPad – 768×1024)\n3. Navigate to https://app.vwo.com\n4. Test all login page interactions",
        "1. Login page layout adapts correctly to tablet screen\n2. No content overflow or misalignment\n3. All form elements are functional and accessible",
        "Medium"
    ),
    (
        "TC-UI-005", "UI / UX",
        "VWO product announcement banner is displayed correctly on the login page",
        "1. User is on the login page\n2. An active product announcement is configured",
        "1. Navigate to https://app.vwo.com\n2. Observe the login page for a product announcement banner",
        "1. Product announcement banner is visible at the top or designated area\n2. Banner content is correct and legible\n3. Banner does not obscure login form elements",
        "Low"
    ),
    (
        "TC-UI-006", "UI / UX",
        "Loading indicator is displayed while authentication is being processed",
        "1. User is on the login page with valid credentials ready",
        "1. Navigate to https://app.vwo.com\n2. Enter valid credentials\n3. Click 'Login'\n4. Observe the UI immediately after click",
        "1. A loading spinner or progress indicator is displayed after clicking Login\n2. The Login button is disabled to prevent double-submission\n3. Indicator disappears once the response is received",
        "Medium"
    ),
    (
        "TC-UI-007", "UI / UX",
        "VWO logo and branding elements are consistent with brand guidelines",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Visually inspect the VWO logo, color palette, and typography",
        "1. VWO logo is displayed correctly and is not distorted\n2. Color scheme matches VWO brand guidelines\n3. Font styles are consistent with the design system",
        "Low"
    ),
    (
        "TC-UI-008", "UI / UX",
        "Password show/hide toggle (eye icon) reveals and masks password correctly",
        "1. Password show/hide toggle is present on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter text in the password field\n3. Click the eye icon / Show Password toggle\n4. Click the icon again to hide the password",
        "1. Password text is revealed in plain text when toggle is clicked (show state)\n2. Password is masked again when toggle is clicked again (hide state)\n3. Toggle icon changes to reflect the current state",
        "Medium"
    ),
    (
        "TC-UI-009", "UI / UX",
        "Login page renders correctly at 1366×768 screen resolution",
        "1. Test machine or browser at 1366×768 resolution",
        "1. Set browser/screen to 1366×768 resolution\n2. Navigate to https://app.vwo.com\n3. Inspect the page for layout issues",
        "1. Login form is fully visible and not clipped\n2. No horizontal scroll bar is present\n3. All elements are correctly positioned",
        "Medium"
    ),
    (
        "TC-UI-010", "UI / UX",
        "Login page renders correctly at 1920×1080 screen resolution",
        "1. Test machine or browser at 1920×1080 resolution",
        "1. Set browser/screen to 1920×1080 resolution\n2. Navigate to https://app.vwo.com\n3. Inspect the page for layout issues",
        "1. Login form is centered and well-proportioned\n2. No excessive whitespace or misaligned elements\n3. All elements are correctly visible",
        "Medium"
    ),

    # ── INTEGRATION ──────────────────────────────────────────────────────────
    (
        "TC-INT-001", "Integration",
        "User is redirected to the personalized VWO dashboard immediately after successful login",
        "1. User has valid credentials\n2. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Enter valid email and password\n3. Click 'Login'\n4. Observe the post-authentication redirect",
        "1. Successful authentication triggers an immediate redirect to the VWO dashboard\n2. Dashboard is personalized showing user's account name and context\n3. Redirect happens within 3 seconds",
        "High"
    ),
    (
        "TC-INT-002", "Integration",
        "Recent session activity and context is preserved and shown after re-login",
        "1. User has previously logged in and interacted with VWO (e.g., viewed campaigns)",
        "1. Complete any activity in VWO (e.g., view an experiment)\n2. Log out\n3. Log in again with the same credentials\n4. Observe the dashboard for context restoration",
        "1. Dashboard displays recent activity from the previous session\n2. User context (last viewed page, recent experiments) is preserved\n3. No data loss between sessions",
        "Medium"
    ),
    (
        "TC-INT-003", "Integration",
        "Login success and failure events are tracked in the connected analytics platform",
        "1. Analytics integration is configured\n2. Access to analytics platform event logs",
        "1. Perform a successful login\n2. Perform a failed login attempt\n3. Check the analytics platform (or browser network tab) for tracked events",
        "1. Login success event is recorded in analytics\n2. Login failure event is recorded in analytics\n3. Events contain appropriate metadata (timestamp, event type)\n4. No PII (passwords, tokens) is included in analytics events",
        "Medium"
    ),
    (
        "TC-INT-004", "Integration",
        "Customer support link or help option is accessible from the login page",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Look for a 'Help', 'Support', or 'Contact Us' link on the login page\n3. Click the link",
        "1. A support or help option is visible on the login page\n2. Clicking it navigates to the support page or opens a help widget\n3. The link is functional without requiring authentication",
        "Low"
    ),
    (
        "TC-INT-005", "Integration",
        "Free Trial / Sign Up CTA navigates to the registration page",
        "1. User is on the login page",
        "1. Navigate to https://app.vwo.com\n2. Locate the 'Start Free Trial', 'Sign Up', or 'Create Account' CTA\n3. Click the CTA",
        "1. A Free Trial / Sign Up CTA is visible on the login page\n2. Clicking CTA navigates to the VWO registration/free trial page\n3. The registration page loads correctly",
        "Medium"
    ),

    # ── END-TO-END FLOWS ────────────────────────────────────────────────────
    (
        "TC-E2E-001", "End-to-End Flow",
        "Complete new user journey: registration → email verification → first login → onboarding → dashboard",
        "1. A new VWO account has NOT been created\n2. A valid email address is available",
        "1. Navigate to https://app.vwo.com\n2. Click the 'Start Free Trial' or 'Sign Up' CTA\n3. Complete the registration form with valid details\n4. Submit the registration form\n5. Open the verification email and click the verification link\n6. Complete the email verification step\n7. Log in for the first time with new credentials\n8. Complete the onboarding wizard (if presented)\n9. Access the VWO dashboard",
        "1. Registration completes successfully\n2. Verification email is received and verification is successful\n3. First login works correctly\n4. Onboarding guidance is presented to new users\n5. Dashboard is accessible and personalized",
        "High"
    ),
    (
        "TC-E2E-002", "End-to-End Flow",
        "Complete returning user journey: login → dashboard → view running experiments → review reports",
        "1. User has a registered VWO account with at least one running experiment",
        "1. Navigate to https://app.vwo.com\n2. Log in with valid credentials\n3. Confirm redirect to dashboard\n4. Navigate to the Experiments section\n5. Open a running experiment\n6. Navigate to the Reports section for that experiment\n7. Review the statistical data",
        "1. Login succeeds and dashboard loads\n2. Experiments section shows correctly\n3. Running experiment details are visible\n4. Reports load with accurate data\n5. All navigation is seamless",
        "High"
    ),
    (
        "TC-E2E-003", "End-to-End Flow",
        "Complete error recovery flow: failed login → forgot password → reset password → login with new password",
        "1. User has a registered account\n2. User does not know their current password",
        "1. Navigate to https://app.vwo.com\n2. Attempt to log in with the correct email but wrong password\n3. Observe error message\n4. Click 'Forgot Password'\n5. Enter the registered email on the recovery page\n6. Submit the forgot password request\n7. Receive reset email and click the reset link\n8. Enter a new valid password and confirm it\n9. Click 'Reset Password'\n10. Log in using the new password",
        "1. Initial login fails with appropriate error message\n2. Forgot Password flow initiates correctly\n3. Reset email is received\n4. Password is reset successfully\n5. Login with new password succeeds\n6. Dashboard is accessible",
        "High"
    ),
    (
        "TC-E2E-004", "End-to-End Flow",
        "Complete 2FA flow: login → 2FA prompt → valid code entry → dashboard access",
        "1. User has 2FA enabled on their account",
        "1. Navigate to https://app.vwo.com\n2. Enter valid email and password\n3. Click 'Login'\n4. Observe 2FA verification prompt\n5. Open authenticator app and retrieve the current 6-digit code\n6. Enter the valid 2FA code\n7. Click 'Verify'",
        "1. Login with email/password passes\n2. 2FA prompt appears correctly\n3. Valid 2FA code is accepted\n4. User is redirected to the VWO dashboard",
        "High"
    ),
    (
        "TC-E2E-005", "End-to-End Flow",
        "Complete enterprise SSO flow: SSO initiation → identity provider auth → VWO dashboard access",
        "1. Enterprise SSO (SAML/OAuth) is configured\n2. User has valid enterprise account credentials",
        "1. Navigate to https://app.vwo.com\n2. Enter enterprise email or click 'Sign in with SSO'\n3. Be redirected to the enterprise identity provider login page\n4. Complete authentication on the identity provider\n5. Be redirected back to VWO",
        "1. SSO flow initiates correctly\n2. Redirect to identity provider happens seamlessly\n3. Identity provider authentication succeeds\n4. Redirect back to VWO is successful\n5. Dashboard loads with correct user context and permissions",
        "High"
    ),
]

# ── Sheet: Cover ─────────────────────────────────────────────────────────────
def make_cover(wb):
    ws = wb.active
    ws.title = "Cover"
    ws.sheet_view.showGridLines = False

    bg = PatternFill("solid", fgColor="1F3864")
    for r in range(1, 26):
        for c in range(1, 6):
            ws.cell(row=r, column=c).fill = bg

    for col_letter, width in [("A", 5), ("B", 45), ("C", 40)]:
        ws.column_dimensions[col_letter].width = width

    def cset(row, col, val, fnt, aln=None):
        cell = ws.cell(row=row, column=col, value=val)
        cell.font = fnt
        if aln:
            cell.alignment = aln
        return cell

    ws.merge_cells("B3:C3")
    cset(3, 2, "VWO A/B Testing Platform – app.vwo.com",
         Font(name="Calibri", bold=True, size=22, color="FFFFFF"), C_ALIGN)

    ws.merge_cells("B4:C4")
    cset(4, 2, "Comprehensive Test Cases Document",
         Font(name="Calibri", bold=True, size=16, color="F2C94C"), C_ALIGN)

    ws.merge_cells("B5:C5")
    cset(5, 2, "Template: FTC02 – PRD to Test Cases (Comprehensive)",
         Font(name="Calibri", size=11, color="A9C4E4", italic=True), C_ALIGN)

    ws.merge_cells("B7:C7")
    divider = ws["B7"]
    divider.value = "─" * 60
    divider.font = Font(color="F2C94C")
    divider.alignment = C_ALIGN

    meta = [
        ("Product",          "VWO A/B Testing Platform (app.vwo.com)"),
        ("Document Type",    "Comprehensive Test Cases"),
        ("Template Used",    "FTC02 – PRD to Test Cases (Comprehensive)"),
        ("Version",          "1.0"),
        ("Prepared By",      "Apparao Maroju"),
        ("Date",             "March 31, 2026"),
        ("Status",           "Draft"),
        ("Total Test Cases", str(len(TESTCASES))),
    ]
    lf = Font(name="Calibri", bold=True, color="F2C94C", size=11)
    vf = Font(name="Calibri", color="FFFFFF", size=11)
    for i, (label, value) in enumerate(meta, start=9):
        ws.cell(row=i, column=2, value=label).font = lf
        ws.cell(row=i, column=2).alignment = L_ALIGN
        ws.cell(row=i, column=3, value=value).font = vf
        ws.cell(row=i, column=3).alignment = L_ALIGN

    ws.row_dimensions[3].height = 35
    ws.row_dimensions[4].height = 28

    # Legend
    l_row = 19
    ws.cell(row=l_row, column=2, value="Priority Legend:").font = lf
    for idx, (p, c) in enumerate(PRIO_COLOR.items()):
        cell = ws.cell(row=l_row + 1, column=2 + idx, value=p)
        cell.font = Font(name="Calibri", bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill("solid", fgColor=c)
        cell.alignment = C_ALIGN
        cell.border = THIN


# ── Sheet: Test Cases ────────────────────────────────────────────────────────
def make_testcases_sheet(wb):
    ws = wb.create_sheet("Test Cases")
    ws.sheet_view.showGridLines = False

    # Banner row 1
    ws.merge_cells("A1:H1")
    t = ws["A1"]
    t.value = "VWO A/B Testing Platform – Comprehensive Test Cases  |  app.vwo.com"
    t.font = Font(name="Calibri", bold=True, size=13, color="FFFFFF")
    t.fill = PatternFill("solid", fgColor="1F3864")
    t.alignment = C_ALIGN
    ws.row_dimensions[1].height = 28

    # Sub-banner row 2
    ws.merge_cells("A2:H2")
    s = ws["A2"]
    s.value = (f"Total Test Cases: {len(TESTCASES)}  |  "
               "Prepared By: Apparao Maroju  |  Date: March 31, 2026  |  "
               "Template: FTC02 – PRD to Test Cases (Comprehensive)")
    s.font = Font(name="Calibri", size=10, italic=True, color="FFFFFF")
    s.fill = PatternFill("solid", fgColor="2E4DA0")
    s.alignment = C_ALIGN
    ws.row_dimensions[2].height = 18

    # Column headers
    headers = [
        "TID", "Category", "Test Case Description",
        "Pre-conditions", "Test Steps",
        "Expected Result", "Priority", "Status"
    ]
    col_widths = [16, 24, 45, 35, 55, 55, 11, 12]
    for col, (h, w) in enumerate(zip(headers, col_widths), start=1):
        ws.column_dimensions[get_column_letter(col)].width = w
        cell = ws.cell(row=3, column=col, value=h)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = C_ALIGN
        cell.border = THIN
    ws.row_dimensions[3].height = 22

    # Data rows
    for i, (tid, cat, desc, pre, steps, expected, priority) in enumerate(TESTCASES, start=4):
        fill = ALT_FILL if (i % 2 == 0) else WHITE_FILL
        row_values = [tid, cat, desc, pre, steps, expected, priority, "Not Run"]

        for col, val in enumerate(row_values, start=1):
            cell = ws.cell(row=i, column=col, value=val)
            cell.border = THIN
            cell.fill = fill

            if col in (1,):  # TID
                cell.font = BOLD_FONT
                cell.alignment = C_ALIGN
            elif col in (7, 8):  # Priority, Status
                cell.font = Font(name="Calibri", bold=True, size=10, color="FFFFFF")
                cell.alignment = C_ALIGN
            else:
                cell.font = BODY_FONT
                cell.alignment = L_ALIGN

        # Color-code Priority
        p_cell = ws.cell(row=i, column=7)
        p_cell.fill = PatternFill("solid", fgColor=PRIO_COLOR.get(priority, "595959"))

        # Color-code Category
        c_cell = ws.cell(row=i, column=2)
        c_cell.font = Font(name="Calibri", bold=True, size=10, color="FFFFFF")
        c_cell.fill = PatternFill("solid", fgColor=CAT_COLOR.get(cat, "2E4DA0"))
        c_cell.alignment = C_ALIGN

        # Status – default gray
        s_cell = ws.cell(row=i, column=8)
        s_cell.fill = PatternFill("solid", fgColor="595959")

        ws.row_dimensions[i].height = 90

    ws.freeze_panes = "A4"
    ws.auto_filter.ref = f"A3:H{3 + len(TESTCASES)}"


# ── Sheet: Summary ────────────────────────────────────────────────────────────
def make_summary_sheet(wb):
    from collections import Counter
    ws = wb.create_sheet("Summary")
    ws.sheet_view.showGridLines = False

    ws.merge_cells("A1:D1")
    t = ws["A1"]
    t.value = "Test Cases – Summary Dashboard"
    t.font = Font(name="Calibri", bold=True, size=14, color="FFFFFF")
    t.fill = PatternFill("solid", fgColor="1F3864")
    t.alignment = C_ALIGN
    ws.row_dimensions[1].height = 30

    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 14
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 14

    cat_counts  = Counter(tc[1] for tc in TESTCASES)
    prio_counts = Counter(tc[6] for tc in TESTCASES)

    def write_section(start_row, col_a, heading, data_dict, color):
        col_b = col_a + 1
        ws.merge_cells(start_row=start_row, start_column=col_a,
                       end_row=start_row, end_column=col_b)
        hc = ws.cell(row=start_row, column=col_a, value=heading)
        hc.font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
        hc.fill = PatternFill("solid", fgColor=color)
        hc.alignment = C_ALIGN
        hc.border = THIN
        for i, (key, cnt) in enumerate(sorted(data_dict.items(), key=lambda x: -x[1]), 1):
            r = start_row + i
            fill = ALT_FILL if i % 2 == 0 else WHITE_FILL
            ka = ws.cell(row=r, column=col_a, value=key)
            kb = ws.cell(row=r, column=col_b, value=cnt)
            for cell in (ka, kb):
                cell.font = BODY_FONT
                cell.border = THIN
                cell.fill = fill
            ka.alignment = L_ALIGN
            kb.alignment = C_ALIGN
        return start_row + len(data_dict) + 2

    next_r = write_section(3, 1, "Category (Test Case Count)", cat_counts, "2E4DA0")
    write_section(3, 3, "Priority (Count)", prio_counts, "C00000")

    # Totals
    total_r = next_r
    tc = ws.cell(row=total_r, column=1, value="TOTAL TEST CASES")
    tc.font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    tc.fill = PatternFill("solid", fgColor="1F3864")
    tc.alignment = L_ALIGN
    tc.border = THIN
    vc = ws.cell(row=total_r, column=2, value=len(TESTCASES))
    vc.font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    vc.fill = PatternFill("solid", fgColor="1F3864")
    vc.alignment = C_ALIGN
    vc.border = THIN


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    wb = Workbook()
    make_cover(wb)
    make_testcases_sheet(wb)
    make_summary_sheet(wb)
    wb.save(OUTPUT_PATH)
    print(f"SUCCESS: {OUTPUT_PATH}")
    print(f"Total test cases: {len(TESTCASES)}")

if __name__ == "__main__":
    main()
