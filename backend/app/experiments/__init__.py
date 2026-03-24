"""Experiment handler registry."""

from __future__ import annotations

from ..models.experiment import ExperimentId
from .base import BaseExperiment
from .budget_groupe import BudgetGroupeExperiment
from .conseil_crise import ConseilCriseExperiment
from .construction_regle import ConstructionRegleExperiment
from .enquete_collective import EnqueteCollectiveExperiment
from .information_fragmentee import InformationFragmenteeExperiment
from .loi_du_groupe import LoiDuGroupeExperiment
from .negociation_ressources import NegociationRessourcesExperiment
from .pouvoir_tourne import PouvoirTourneExperiment
from .repartition_priorites import RepartitionPrioritesExperiment
from .traitre_invisible import TraitreInvisibleExperiment

_REGISTRY: dict[ExperimentId, BaseExperiment] = {
    ExperimentId.BUDGET_GROUPE: BudgetGroupeExperiment(),
    ExperimentId.CONSEIL_CRISE: ConseilCriseExperiment(),
    ExperimentId.TRAITRE_INVISIBLE: TraitreInvisibleExperiment(),
    ExperimentId.ENQUETE_COLLECTIVE: EnqueteCollectiveExperiment(),
    ExperimentId.NEGOCIATION_RESSOURCES: NegociationRessourcesExperiment(),
    ExperimentId.POUVOIR_TOURNE: PouvoirTourneExperiment(),
    ExperimentId.INFORMATION_FRAGMENTEE: InformationFragmenteeExperiment(),
    ExperimentId.REPARTITION_PRIORITES: RepartitionPrioritesExperiment(),
    ExperimentId.CONSTRUCTION_REGLE: ConstructionRegleExperiment(),
    ExperimentId.LOI_DU_GROUPE: LoiDuGroupeExperiment(),
}


def get_experiment_handler(experiment_id: ExperimentId) -> BaseExperiment:
    """Return the handler for a given experiment ID."""
    handler = _REGISTRY.get(experiment_id)
    if handler is None:
        raise ValueError(f"No handler registered for experiment: {experiment_id}")
    return handler


def get_all_definitions():
    """Return all experiment definitions."""
    return [h.definition() for h in _REGISTRY.values()]
