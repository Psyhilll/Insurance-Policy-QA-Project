# ============================================================
# SafeGuard Insurance – Element Locators
# All CSS selectors and locators in one place.
# If the UI changes, update here — tests stay untouched.
# ============================================================


class LoginLocators:
    EMAIL_INPUT    = "#email"
    PASSWORD_INPUT = "#password"
    SUBMIT_BUTTON  = "button[type='submit']"
    ERROR_ALERT    = ".alert-danger"
    SUCCESS_ALERT  = ".alert-success"


class RegisterLocators:
    FIRST_NAME     = "input[name='first_name']"
    LAST_NAME      = "input[name='last_name']"
    EMAIL          = "input[name='email']"
    PHONE          = "input[name='phone']"
    DATE_OF_BIRTH  = "input[name='date_of_birth']"
    PASSWORD       = "input[name='password']"
    CONFIRM_PASS   = "input[name='confirm_password']"
    SUBMIT_BUTTON  = "button[type='submit']"
    ERROR_ALERT    = ".alert-danger"
    SUCCESS_ALERT  = ".alert-success"
    LOGIN_LINK     = "a[href='/login']"


class DashboardLocators:
    WELCOME_HEADER   = ".page-header h4"
    STAT_CARDS       = ".stat-card"
    POLICIES_TABLE   = "table"
    QUICK_ACTIONS    = ".btn"
    NAV_QUOTE        = "a[href='/quote']"
    NAV_POLICIES     = "a[href='/policies']"
    NAV_CLAIMS       = "a[href='/claims']"
    NAV_TRACK        = "a[href='/claim-tracking']"
    NAV_LOGOUT       = "a[href='/logout']"


class QuoteLocators:
    POLICY_TYPE      = "select[name='policy_type']"
    COVERAGE_AMOUNT  = "input[name='coverage_amount']"
    AGE              = "input[name='age']"
    SUBMIT_BUTTON    = "button[type='submit']"
    RESULT_CARD      = ".border-success"
    PREMIUM_DISPLAY  = ".table-success td:last-child"
    PURCHASE_BUTTON  = "a.btn-success"
    ERROR_ALERT      = ".alert-danger"


class PurchaseLocators:
    START_DATE       = "input[name='start_date']"
    END_DATE         = "input[name='end_date']"
    CONFIRM_BUTTON   = "button[type='submit']"
    SUCCESS_ALERT    = ".alert-success"
    ERROR_ALERT      = ".alert-danger"


class ClaimsLocators:
    POLICY_SELECT    = "select[name='policy_id']"
    CLAIM_AMOUNT     = "input[name='claim_amount']"
    CLAIM_REASON     = "textarea[name='claim_reason']"
    SUBMIT_BUTTON    = "button[type='submit']"
    SUCCESS_ALERT    = ".alert-success"
    ERROR_ALERT      = ".alert-danger"
    NO_POLICY_MSG    = ".text-center"


class ClaimTrackingLocators:
    CLAIMS_TABLE     = "table"
    CLAIM_ROWS       = "tbody tr"
    STATUS_BADGES    = ".badge"
    EMPTY_STATE      = ".text-center"


class AdminLocators:
    STAT_CARDS       = ".stat-card"
    CUSTOMERS_LINK   = "a[href='/admin/customers']"
    CLAIMS_LINK      = "a[href='/admin/claims']"
    APPROVE_BUTTON   = "button[value='Approved']"
    REJECT_BUTTON    = "button[value='Rejected']"
    CLAIMS_TABLE     = "table"
