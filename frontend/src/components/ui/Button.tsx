import { type ButtonHTMLAttributes } from "react";

type Variant = "primary" | "secondary" | "link" | "icon";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  danger?: boolean;
};

export function Button({
  variant = "primary",
  danger = false,
  className = "",
  children,
  ...rest
}: Props) {
  const classes = [
    "btn",
    variant,
    danger ? "danger" : "",
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <button type="button" {...rest} className={classes}>
      {children}
    </button>
  );
}
