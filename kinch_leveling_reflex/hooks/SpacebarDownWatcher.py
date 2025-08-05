import reflex as rx
from reflex.utils import imports

class SpacebarDownWatcher(rx.Fragment):
    """Un componente que escucha la barra espaciadora y dispara un evento Reflex."""

    # El event handler que se llamará cuando se presione espacio
    on_space: rx.EventHandler

    def add_imports(self) -> imports.ImportDict:
        return {
            "react": [imports.ImportVar(tag="useEffect")],
        }

    def add_hooks(self) -> list[str | rx.Var]:
        return [
            f"""
useEffect(() => {{
  const handleKeyDown = (event) => {{
    if (event.key === " ") {{
      {str(rx.Var.create(self.event_triggers['on_space']))}();
    }}
  }};
  window.addEventListener("keydown", handleKeyDown);
  return () => {{
    window.removeEventListener("keydown", handleKeyDown);
  }};
}}, []);
"""
        ]