import { FC } from "react";
import HealthScore from "@/components/HealthScore";
import { Activity, RefreshCw } from "lucide-react";
import { NutrientCard } from "./NutrientCard";
import { useGetMeasurements } from "@/api/useGetMeasurements";
import { Button } from "./ui/button";

const Dashboard: FC = () => {
  const { data: measurements, status, refetch, isRefetching, aiAnalysis } = useGetMeasurements();

  if (status === "pending" || status === "error") {
    return (
      <div className="flex items-center justify-center h-64">
        <Activity className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold">Today's Overview</h2>
        <Button
          variant="outline"
          size="sm"
          onClick={() => refetch()}
          disabled={isRefetching}
          className="gap-2"
        >
          <RefreshCw className={`h-4 w-4 ${isRefetching ? "animate-spin" : ""}`} />
          Refresh
        </Button>
      </div>

      <HealthScore />

      {/* AI Insights Section */}
      {aiAnalysis && aiAnalysis.length > 0 && (
        <div className="rounded-lg border bg-card text-card-foreground shadow-sm p-4">
          <div className="flex flex-col space-y-1.5 pb-2">
            <h3 className="font-semibold leading-none tracking-tight flex items-center gap-2">
              <Activity className="h-4 w-4 text-primary" />
              AI Insights
            </h3>
          </div>
          <ul className="list-disc pl-5 text-sm space-y-1">
            {aiAnalysis.map((insight: string, idx: number) => (
              <li key={idx} className="text-muted-foreground">
                {insight}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="grid gap-2">
        {measurements.map((m) => (
          <NutrientCard measurement={m} key={m.name} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
