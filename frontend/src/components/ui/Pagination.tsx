import { Button } from "@/components/ui/Button";

type Props = {
  page: number;
  totalCount: number;
  pageSize: number;
  onPageChange: (page: number) => void;
  disabled?: boolean;
};

export function Pagination(props: Props) {
  const totalPages = Math.ceil(props.totalCount / props.pageSize);

  if (totalPages <= 1) return null;

  return (
    <div className="pagination">
      <Button
        variant="secondary"
        disabled={props.page <= 1 || props.disabled}
        onClick={() => props.onPageChange(props.page - 1)}
      >
        ← Previous
      </Button>
      <span className="pagination-info">
        Page {props.page} of {totalPages} ({props.totalCount} patients)
      </span>
      <Button
        variant="secondary"
        disabled={props.page >= totalPages || props.disabled}
        onClick={() => props.onPageChange(props.page + 1)}
      >
        Next →
      </Button>
    </div>
  );
}
