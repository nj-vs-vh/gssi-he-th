from matplotlib import pyplot as plt
from astropy.visualization import quantity_support  # type: ignore

quantity_support()


def label_axes(ax: plt.Axes, xlabel: str | None = None, ylabel: str | None = None):
    for label, getter, setter in (
        (xlabel, ax.get_xlabel, ax.set_xlabel),
        (ylabel, ax.get_ylabel, ax.set_ylabel),
    ):
        if label is None:
            continue
        units_label = getter().strip()
        if not units_label or units_label == "$\mathrm{}$":
            units = ""
        else:
            units = f" [{units_label}]"
        setter(f"$ {label} $" + units)
