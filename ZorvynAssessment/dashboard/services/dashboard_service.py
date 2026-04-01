from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncMonth

from transactions.models import Transaction


class DashboardService:
    """Business logic for dashboard analytics aggregations."""

    @staticmethod
    def get_user_analytics(user):
        """Return aggregated analytics payload for a user's active transactions."""
        user_transactions = Transaction.objects.filter(user=user, is_deleted=False)

        totals = user_transactions.values('type').annotate(total=Sum('amount'))
        totals_map = {row['type']: row['total'] for row in totals}

        total_income = totals_map.get(Transaction.Type.INCOME, 0)
        total_expense = totals_map.get(Transaction.Type.EXPENSE, 0)

        category_breakdown = {
            row['category']: row['total']
            for row in (
                user_transactions.values('category')
                .annotate(total=Sum('amount'))
                .order_by('category')
            )
        }

        recent_transactions = list(
            user_transactions.values('id', 'amount', 'type', 'category', 'date', 'notes')[:5]
        )

        monthly_trends = [
            {
                'month': row['month'].strftime('%Y-%m'),
                'income': row['income'] or 0,
                'expense': row['expense'] or 0,
                'net': (row['income'] or 0) - (row['expense'] or 0),
                'transaction_count': row['transaction_count'],
            }
            for row in (
                user_transactions.annotate(month=TruncMonth('date'))
                .values('month')
                .annotate(
                    income=Sum('amount', filter=Q(type=Transaction.Type.INCOME)),
                    expense=Sum('amount', filter=Q(type=Transaction.Type.EXPENSE)),
                    transaction_count=Count('id'),
                )
                .order_by('month')
            )
        ]

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': total_income - total_expense,
            'category_breakdown': category_breakdown,
            'recent_transactions': recent_transactions,
            'monthly_trends': monthly_trends,
        }
