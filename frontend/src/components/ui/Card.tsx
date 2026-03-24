import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

export default function Card({ children, className = "", hover = false, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      className={`rounded-xl border border-arena-border bg-arena-surface p-5 ${
        hover ? "cursor-pointer hover:border-arena-accent/50 hover:shadow-lg hover:shadow-arena-accent/5 transition-all duration-200" : ""
      } ${onClick ? "cursor-pointer" : ""} ${className}`}
    >
      {children}
    </div>
  );
}
