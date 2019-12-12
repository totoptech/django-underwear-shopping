from rest_framework import serializers

from accounts.models import PortfolioLike

class PortfolioLikeSerializer(serializers.ModelSerializer):
	class Meta:
		model = PortfolioLike
		fields = (
			'account',
			'uniq_id',
			'lol')