from pyrate_limiter import Duration, Limiter, SQLiteBucket 
from requests_ratelimiter import LimiterSession, RequestRate

__per_second = RequestRate(16,Duration.SECOND)
__per_minute = RequestRate(200,Duration.MINUTE)
__per_hour = RequestRate(7200,Duration.HOUR)
__limiter = Limiter(__per_second, __per_minute, __per_hour)
rate_session = LimiterSession(limiter= __limiter, bucket_class=SQLiteBucket)
