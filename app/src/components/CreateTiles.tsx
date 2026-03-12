import React from "react";
import { MessageCircle, Mic } from "lucide-react";

export type CreateTileKind = "game" | "story" | "character" | "voice";

type CreateTilesProps = {
  includeVoice?: boolean;
  iconSize?: number;
  onSelect: (kind: CreateTileKind) => void;
};

const TILE_CONFIG: Array<{
  kind: CreateTileKind;
  label: string;
  helper: string;
  bgClass: string;
  shadowColor: string;
  Icon: React.ComponentType<{ size?: number; className?: string }>;
}> = [
  {
    kind: "character",
    label: "Character",
    helper: "Create a storytelling experience",
    bgClass: "!bg-yellow-300",
    shadowColor: "#facc15",
    Icon: MessageCircle,
  },
  {
    kind: "voice",
    label: "Voice",
    helper: "Clone a voice",
    bgClass: "!bg-red-400",
    shadowColor: "#ef4444",
    Icon: Mic,
  },
];

export const CreateTiles = ({
  includeVoice = true,
  iconSize = 24,
  onSelect,
}: CreateTilesProps) => {
  const tiles = includeVoice ? TILE_CONFIG : TILE_CONFIG.filter((t) => t.kind !== "voice");

  return (
    <div className="grid grid-cols-2 gap-4">
      {tiles.map(({ kind, label, helper, bgClass, shadowColor, Icon }) => (
        <button
          key={kind}
          type="button"
          className={`retro-btn w-full text-base flex-col gap-2 text-black ${bgClass}`}
          style={{ ["--shadow-color" as any]: shadowColor }}
          onClick={() => onSelect(kind)}
        >
          <Icon size={iconSize} className="shrink-0" />
          <span className="inline-flex items-center uppercase text-sm gap-2">{label}</span>
          <span className="text-xs font-medium opacity-80">{helper}</span>
        </button>
      ))}
    </div>
  );
};
