import { StudentCard, TaskPriority } from "./types";

// Codes from Smarteducafe_Elite_Learning_System_Master_Knowledge_v1.md —
// keep in sync with PROGRAM_CATALOG in apps/api/app/models/student_intelligence.py.
export const PROGRAM_LABELS: Record<string, string> = {
  SMART_CLASS: "Smart Class",
  INTENSIF_CLASS: "Intensif Class",
  EXCLUSIVE_CLASS: "Exclusive Class",
  EXCLUSIVE_KEDINASAN: "Exclusive + Kedinasan",
};

export const MOCK_STUDENTS: StudentCard[] = [
  {
    id: "SEC-2026-00124",
    name: "Dila",
    dreamTarget: "Ilmu Komunikasi UNPAD",
    currentScore: 557,
    targetScore: 700,
    scoreGap: 143,
    status: "YELLOW",
    program: "INTENSIF_CLASS",
    readinessScore: 67,
    primaryBottleneck: "Penalaran Matematika",
  },
  {
    id: "SEC-2026-00131",
    name: "Keyla",
    dreamTarget: "Kriminologi UI",
    currentScore: 420,
    targetScore: 650,
    scoreGap: 230,
    status: "ORANGE",
    program: "EXCLUSIVE_CLASS",
    readinessScore: 48,
    primaryBottleneck: "Penalaran Matematika",
  },
];

export const MOCK_PRIORITIES: TaskPriority[] = [
  {
    id: "TSK-001",
    title: "Campaign Foundation — brief konten",
    projectName: "Marketing SmartEduCafe",
    dueDate: "Besok",
    definitionOfDone: "3 draft caption + 1 moodboard visual disetujui lead",
    progress: 60,
    status: "IN_PROGRESS",
  },
  {
    id: "TSK-002",
    title: "Uji My Day dengan 2 contributor",
    projectName: "SKLOS Local Pilot",
    dueDate: "Hari ini",
    definitionOfDone: "Feedback usability dicatat di Team Room",
    progress: 20,
    status: "TODO",
  },
  {
    id: "TSK-003",
    title: "Review modul Numerasi minggu 3",
    projectName: "Kurikulum Foundation",
    dueDate: "Lusa",
    definitionOfDone: "Checklist QA modul terisi penuh",
    progress: 80,
    status: "IN_PROGRESS",
  },
];
