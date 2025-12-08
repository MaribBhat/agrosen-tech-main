export type MeasurementUnit = {
  low: number;
  high: number;
  unit: string;
};

export type Measurement = {
  name: string;
  value: number;
  unit: MeasurementUnit;
  label?: string;
  variant?: "default" | "secondary" | "destructive" | "outline";
};

export enum Substance {
  Nitrogen = "nitrogen",
  Potassium = "potassium",
  Phosphorus = "phosphorus",
  SoilMoisture = "soil_moisture",
  SoilMoisture2 = "soil_moisture_2",
}
