rebuild:
	./scripts/rebuild_env.sh
check:
	./scripts/full_check.sh
guard:
	./scripts/scan_override.sh
hooks:
	chmod +x .git/hooks/pre-commit
structure:
	./scripts/show_structure.sh
reset:
	./scripts/reset_state.sh
.PHONY: rebuild check guard hooks structure reset
