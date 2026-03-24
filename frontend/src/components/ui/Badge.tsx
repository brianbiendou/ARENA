interface Props {
  label: string;
  color?: string;
  variant?: "solid" | "outline";
}

export default function Badge({ label, color, variant = "solid" }: Props) {
  const style = color
    ? variant === "solid"
      ? { backgroundColor: `${color}20`, color, borderColor: `${color}40` }
      : { borderColor: `${color}60`, color }
    : {};

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${
        color ? "" : "bg-arena-accent/20 text-arena-accent-light border-arena-accent/40"
      }`}
      style={style}
    >
      {label}
    </span>
  );
}
