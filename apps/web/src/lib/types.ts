export type Role = "CONTRIBUTOR" | "TEAM_LEADER" | "ADMIN";

export interface TaskPriority {
  id: string;
  title: string;
  projectName: string;
  dueDate: string;
  definitionOfDone: string;
  progress: number;
  status: "TODO" | "IN_PROGRESS" | "BLOCKED" | "DONE";
}

export interface DailyUpdatePayload {
  taskId: string;
  progress: number;
  output: string;
  impact: string;
  energyLevel: number;
  nextAction: string;
}

export interface BlockerPayload {
  taskId: string;
  description: string;
  severity: "LOW" | "MEDIUM" | "HIGH";
  impact: string;
  helpNeeded: string;
}

// SEC Student Intelligence — separate bounded context from the Kaizen
// loop types above. See docs/01-SEC-Student-Intelligence-Sync.md.
export interface StudentCard {
  id: string;
  name: string;
  dreamTarget: string;
  currentScore: number;
  targetScore: number;
  scoreGap: number;
  status: "GREEN" | "YELLOW" | "ORANGE" | "RED";
  program: string | null;
  readinessScore: number | null;
  primaryBottleneck: string | null;
}

export interface SyncRunSummary {
  id: string;
  sourceFile: string;
  inserted: number;
  updated: number;
  duplicate: number;
  review: number;
  blocked: number;
  createdAt: string;
}
