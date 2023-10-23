import pandas as pd

ZERO_INTERVAL = pd.Timedelta(microseconds=0)


class Resampler:
    def __init__(
        self,
        df: pd.DataFrame,
        on: str,
        resolution: pd.Timedelta,
    ):
        self.df = df
        self.on = on
        self.resolution = resolution

    def agg(self, method: str, edge: str = "left"):
        """Aggregate (downsample) time series.
        For example, if the input is a time series H with
        hourly resolution, then we can aggregate, using
        the mean, to daily resolution, and produce a new
        time series D. In other words:

            - Input:    H(hour)
            - Output:   D(day) = mean( H(hour) for hour in day)

        Args:
            method (str): Aggregation method ("mean", "sum", etc.)
            edge (str, optional): Which side of the interval
                to use as label ("left" or "right").
                Defaults to "left".
        """
        # to aggregate (downsample), the largest
        # time interval in the original series must
        # be smaller or equal to the specified resolution
        df = self.df.sort_values(by=self.on)
        max_time_diff = self.df[self.on].diff().max()
        if max_time_diff > self.resolution:
            raise ValueError(
                f"Aggregation is not possible since the "
                f"downsample resolution '{self.resolution}' "
                f"is smaller than the largest time difference "
                f"in time series ('{max_time_diff}')"
            )

        return (
            df.set_index(keys=self.on)
            .resample(rule=self.resolution, label=edge, closed=edge)
            .aggregate(method, numeric_only=True)
            .reset_index()
        )

    def interpolate(self, method: str = "interpolate"):
        """Interpolate (upsample) time series.
        For example, if the input is a time series D with
        daily resolution, then we can interpolate, using
        a linear function, to hourly resolution, and
        produce a new time series H. In other words:

            - Input:    D(day)
            - Output:   H(hour) = interpolate(hour between day+0 and day+1)

        Args:
            method (str): Interpolation method ("interpolate" (meaning linear),
                "ffill", etc.)
        """
        # pandas doesn't handle empty dataframes very well
        if self.df.empty:
            return self.df

        # to interpolate (upsample), the smallest
        # time interval in the original series must
        # be larger or equal to the specified resolution
        df = self.df.sort_values(by=self.on)
        min_time_diff = df[self.on].diff().min()
        if min_time_diff < self.resolution:
            raise ValueError(
                f"Interpolation is not possible since the "
                f"upsample resolution '{self.resolution}' "
                f"is larger than the smallest time difference "
                f"in time series ('{min_time_diff}')"
            )

        start_time = df[self.on].min()
        end_time = df[self.on].max()

        df = (
            df.set_index(self.on)
            .resample(rule=self.resolution)
            .aggregate(method)
            .reset_index()
        )

        # after resampling, pandas might leave
        # timestamps outside of the original interval
        if not df.empty:
            df = df[df[self.on].between(start_time, end_time)]

        return df

    def granulate(self, edge: str = "left"):
        """Fine-grain (upsample) time series.
        For example, if the input is a time series D with
        daily resolution, then we can granulate to hourly
        resolution, and produce a new time series H.
        In other words:

            - Input:    D(day)
            - Output:   H(hour) = D(day containing hour)


        Args:
            edge (str, optional): Which side of the interval
                to use as label ("left" or "right").
                Defaults to "left".
        """
        # pandas doesn't handle empty dataframes very well
        if self.df.empty:
            return self.df

        df = self.df.sort_values(by=self.on)

        inferred_resolution = pd.Timedelta(
            # needed due to pandas bug https://github.com/pandas-dev/pandas/issues/36769
            pd.tseries.frequencies.to_offset(
                pd.infer_freq(
                    # due to a bug pandas cannot infer frequency
                    # for timezone-aware timestamps
                    df[self.on].dt.tz_convert(None)
                    if df[self.on].dt.tz
                    else df[self.on]
                )
            )
        )

        if edge == "left":
            left_margin = ZERO_INTERVAL
            right_margin = inferred_resolution
        elif edge == "right":
            left_margin = -inferred_resolution
            right_margin = ZERO_INTERVAL
        else:
            raise ValueError(f"Unsupported value {edge} for `edge`")

        df[self.on] = df.apply(
            lambda row: pd.date_range(
                row[self.on] + left_margin,
                row[self.on] + right_margin,
                freq=self.resolution,
                inclusive=edge,
            ),
            axis="columns",
        )

        df = df.explode(column=self.on).reset_index(drop=True)

        return df


def resample(df: pd.DataFrame, on: str, resolution: pd.Timedelta):
    return Resampler(df, on, resolution)
