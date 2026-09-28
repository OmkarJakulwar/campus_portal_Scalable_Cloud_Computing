from rest_framework.permissions import BasePermission


class IsStudentAuthenticated(BasePermission):
    # Allow access only when a ``student_username`` is stored in session.

    def has_permission(self, request, view) -> bool:
        return bool(request.session.get('student_username'))