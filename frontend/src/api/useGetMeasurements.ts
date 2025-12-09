import { Measurement, MeasurementUnit, Substance } from "@/types";
import { useQueries } from "@tanstack/react-query";

export const BASE_URL = import.meta.env.VITE_BASE_API;

// Reads the reading & range endpoints. Combines the result into
// measurement.
export const useGetMeasurements = () => {
  const result = useQueries({
    queries: [GetReadingQuery, GetRangeQuery],
  });

  const [reading, range] = result;

  const data =
    reading.data && range.data
      ? convertToMeasurements(reading.data, range.data)
      : [];
  console.log(result);

  const refetchAll = () => {
    result.forEach((result) => result.refetch());
  };

  const status =
    result.some((result) => result.status !== "success") ?? "success";

  return { refetch: refetchAll, data, status };
};

type Reading = Record<string, any>;

const GetReadingQuery = {
  queryKey: ["reading"],
  queryFn: async (): Promise<Reading> => {
    return fetch(`${BASE_URL}/api/reading`).then((res) => res.json());
  },
};

type Range = Record<Substance, MeasurementUnit>;

const GetRangeQuery = {
  queryKey: ["range"],
  queryFn: async (): Promise<Range> => {
    return fetch(`${BASE_URL}/api/ranges`).then((res) => res.json());
  },
};

function convertToMeasurements(reading: Reading, range: Range): Measurement[] {
  // Iterate over known substances defined in Range
  return Object.entries(range).map(([substance, unit]) => {
    const value = reading[substance];
    const label = reading[`${substance}_label`];

    let variant: Measurement["variant"] = "default";
    if (label) {
      if (label === "Ideal") variant = "default";
      else if (label === "Dry" || label === "Moist") variant = "secondary";
      else variant = "destructive"; // Very Dry, Wet
    }

    return {
      name: substance,
      unit,
      value: typeof value === 'number' ? value : 0, // Ensure number
      label,
      variant
    };
  });
}
