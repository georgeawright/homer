from linguoplotter.codelets.builders import RelationBuilder


class InterspatialRelationBuilder(RelationBuilder):
    @classmethod
    def get_follow_up_class(cls) -> type:
        from linguoplotter.codelets.evaluators.relation_evaluators import (
            InterspatialRelationEvaluator,
        )

        return InterspatialRelationEvaluator
