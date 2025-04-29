from dataclasses import dataclass, asdict

@dataclass
class Recommendation:
    action: str

    def to_dict(self):
        data = asdict(self)
        # Have the recommendation format its reason itself during serialization
        data["reason"] = self.format_reason()
        return data

@dataclass
class SpikeRecommendation(Recommendation):
    latest_volume: float
    avg_volume: float
    latest_price: float
    yesterdays_price: float

    def format_reason(self) -> str:
        if self.action == "Buy":
            return (
                f"Buy. The latest volume, {self.latest_volume}, is much larger than its "
                f"30-day average volume, {self.avg_volume:.2f}, while its latest price, "
                f"${self.latest_price}, is above yesterday's price, ${self.yesterdays_price}"
            )
        else:
            return (
                f"Do not buy. The latest volume, {self.latest_volume}, is not much larger than "
                f"its 30-day average volume, {self.avg_volume:.2f}, or its latest price, "
                f"${self.latest_price}, is below yesterday's price, ${self.yesterdays_price}"
            )

@dataclass
class MomentumRecommendation(Recommendation):
    avg_price: float
    latest_price: float

    def format_reason(self) -> str:
        if self.action == "Buy":
            return (
                f"Buy. The latest price, ${self.latest_price:.2f}, is significantly ahead of "
                f"its 30-day average, ${self.avg_price:.2f}."
            )
        else:
            return (
                f"Do not buy. The latest price, ${self.latest_price:.2f}, is not far enough above "
                f"its 30-day average, ${self.avg_price:.2f}, to justify momentum buying."
            )

@dataclass
class SteadinessRecommendation(Recommendation):
    avg_volatility: float
    avg_volume: float

    def format_reason(self) -> str:
        if self.action == "Buy":
            return (
                f"Buy. The 30-day average volatility is low at {self.avg_volatility:.2f}, "
                f"and the 30-day average volume is high at {self.avg_volume:.2f}."
            )
        else:
            return (
                f"Do not buy. Either the 30-day average volatility is high at {self.avg_volatility:.2f}, "
                f"or the volume is low at {self.avg_volume:.2f}. Conditions do not indicate a stable surge."
            )

@dataclass
class DipRecommendation(Recommendation):
    price_10d: float
    price_5d: float
    latest_price: float
    def format_reason(self) -> str:
        if self.action == "Buy":
            return (
                f"Buy. Its price 10 days ago, ${self.price_10d:.2f}, is 10% greater than "
                f"its price today ${self.latest_price:.2f}, and its price 5 days ago "
                f"${self.price_5d:.2f}, is lower than the latest price."
            )
        else:
            return (
                f"Do not buy. The price 10 days ago is ${self.price_10d:.2f}, "
                f"today's price is ${self.latest_price:.2f}, and the price 5 days ago "
                f"is ${self.price_5d:.2f}. The dip pattern isn't strong enough."
            )


@dataclass
class UnavailableRecommendation(Recommendation):
    def format_reason(self) -> str:
        return "Unable to find data to generate a recommendation. Are you sure your ticker is correct?"