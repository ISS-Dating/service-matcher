import math

from model.entity.base_entity import BaseEntity


class VariableStats(BaseEntity):
    min: float
    max: float
    mean: float
    variance: float
    sample_size: int

    @classmethod
    def from_value(cls, value: float) -> 'VariableStats':
        return cls(min=value, max=value, mean=value, variance=0, sample_size=1)

    def add_value(self, value: float) -> 'VariableStats':
        # using Welford's algorithm
        # https://changyaochen.github.io/welford/
        # https://en.wikipedia.org/wiki/Algorithms_for_calculating_variance

        updated_mean = self.mean + (value - self.mean) / (self.sample_size + 1)
        updated_variance = (self.variance + ((value - self.mean) *
                                             (value - updated_mean) - self.variance) / (self.sample_size + 1))
        return VariableStats(
            min=min(self.min, value),
            max=max(self.max, value),
            mean=updated_mean,
            variance=updated_variance,
            sample_size=self.sample_size + 1
        )

    @property
    def std(self) -> float:
        return math.sqrt(self.variance)

    @property
    def rsd(self) -> float:
        """Coefficient of variation (also known as RSD - relative standard deviation)"""
        return self.std / self.mean if self.mean != 0 else float('nan')
