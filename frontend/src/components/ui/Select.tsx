interface Props {
  label: string;
  value: string;
  options: { value: string; label: string }[];
  onChange: (v: string) => void;
}

export default function Select({ label, value, options, onChange }: Props) {
  return (
    <div className="space-y-1">
      <label className="text-sm text-arena-muted">{label}</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-3 py-2 rounded-lg bg-arena-bg border border-arena-border text-arena-text text-sm focus:border-arena-accent focus:outline-none"
      >
        {options.map((o) => (
          <option key={o.value} value={o.value}>
            {o.label}
          </option>
        ))}
      </select>
    </div>
  );
}
