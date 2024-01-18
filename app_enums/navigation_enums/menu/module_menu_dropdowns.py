from enum import Enum

"""enum class that represent each module menu dropdown"""


class ModulePortletMenu(Enum):
    # ============================================================
    # -----------------------Admin--------------------------------
    GESTION_DES_UTILISATEURS = 'Gestion des utilisateurs',
    EMLOI = 'Emploi',
    ORGANISATION = 'Organisation',
    DIPLOMES = 'Diplômes',
    NATIONALITIES = 'Nationalités',
    CORPORATE_BRANDING = 'Corporate Branding',
    CONFIGURATION = 'Configuration',
    # ============================================================
    # ----------------------GIP-----------------------------------
    CONFIGURATION_GIP = 'Configuration',
    EMPLOYEE_LIST = 'Employee List',
    ADD_EMPLOYEE = 'Add Employee',
    GIP_REPORTS = 'Reports',
    # ============================================================
    # ----------------------Leave---------------------------------
    APPLY = 'Apply',
    MY_LEAVE = 'My Leave',
    ENTITLEMENTS = 'Entitlements',
    LEAVE_REPORTS = 'Reports',
    CONFIGURE = 'Configure',
    LEAVE_LIST = 'Leave List',
    ASSIGN_LEAVE = 'Assign Leave'
    # ============================================================
    # ----------------------Time----------------------------------
    TIME_SHEETS = 'Timesheets',
    ATTENDANCE = 'Attendance',
    TIME_REPORTS = 'Reports',
    PROJECT_INFO = 'Project Info',
    # ============================================================
    # ----------------------Recruitments--------------------------
    CANDIDATES = 'Candidates',
    VACANCIES = 'Vacancies',
    # ============================================================
    # ----------------------Performance---------------------------
    CONFIGURE_PERFORMANCE = 'Configure',
    MANAGE_REVIEWS = 'Manage Reviews',
    MY_TRACKERS = 'My Trackers',
    EMPLOYEE_TRACKERS = 'Employee Trackers',
    # ============================================================
    # ----------------------Maintenance---------------------------
    PURGE_RECORDS = 'Purge_Records',
    ACCESS_RECORDS = 'Access_Records',
    # ============================================================
    # ----------------------Claim---------------------------------
    CLAIM_CONFIGURATION = 'Configuration',
    SUBMIT_CLAIMS = 'Submit Claims',
    MY_CLAIMS = 'My Claims',
    EMPLOYEE_CLAIMS = 'Employee Claims',
    ASSIGN_CLAIM = 'Assign Claim',
