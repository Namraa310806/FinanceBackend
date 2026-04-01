from rest_framework.views import APIView

from finance_dashboard.api_response import success_response
from dashboard.services.dashboard_service import DashboardService
from users.permissions import IsAnalystOrAdmin


class DashboardSummaryView(APIView):
    """Expose dashboard analytics for analyst/admin roles."""

    permission_classes = [IsAnalystOrAdmin]

    def get(self, request):
        analytics = DashboardService.get_user_analytics(request.user)
        return success_response('Dashboard analytics fetched successfully.', analytics)
