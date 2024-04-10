from crum import get_current_request, get_current_user
from bridgekeeper.backends import RulePermissionBackend

class UnidigitalRulesBackend(RulePermissionBackend):

    def has_perm(self, user, perm, obj=None):
        crum_request = get_current_request()
        post_student = crum_request.POST.get("unique_student_identifier", crum_request.POST.get("student", None))
        if post_student == "student":
            return False
        try:
            return self.permission_map[perm].check(user, obj)
        except KeyError:
            return False

    def has_perms(self, user, perms, obj=None):
        for perm in perms:
            if not self.has_perm(user, perm, obj):
                return False
        return True
