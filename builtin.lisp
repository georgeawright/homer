(define input-concept (def-concept :name "input"))
(define text-concept (def-concept :name "text"))

(define views-space
  (def-contextual-space :name "views" :parent_concept None
    :conceptual_spaces (StructureSet)))

(define activity-concept (def-concept :name "activity"))
(define activity-space
  (def-conceptual-space :name "activity" :parent_concept activity-concept))
(define suggest-concept
  (def-concept :name "suggest" :locations (list (Location (list) activity-space))
    :parent_space activity-space :activation 1.0))
(define build-concept
  (def-concept :name "build" :locations (list (Location (list) activity-space))
    :parent_space activity-space :activation 1.0))
(define evaluate-concept
  (def-concept :name "evaluate" :locations (list (Location (list) activity-space))
    :parent_space activity-space))
(define select-concept
  (def-concept :name "select" :locations (list (Location (list) activity-space))
    :parent_space activity-space))
(define publish-concept
  (def-concept :name "publish" :locations (list (Location (list) activity-space))
    :parent_space activity-space))

(define space-type-concept (def-concept :name "space-type"))
(define space-type-space
  (def-conceptual-space :name "space-type" :parent_concept space-type-concept))
(define inner-concept
  (def-concept :name "inner" :locations (list (Location (list) space-type-space))
    :parent_space space-type-space))
(define outer-concept
  (def-concept :name "outer" :locations (list (Location (list) space-type-space))
    :parent_space space-type-space))

(define direction-concept (def-concept :name "direction-type"))
(define direction-space
  (def-conceptual-space :name "direction" :parent_concept direction-concept))
(define forward-concept
  (def-concept :name "forward" :locations (list (Location (list) direction-space))
    :parent_space direction-space))
(define backward-concept
  (def-concept :name "backward" :locations (list (Location (list) direction-space))
    :parent_space direction-space))

(define structure-concept (def-concept :name "structure-type"))
(define structure-space
  (def-conceptual-space :name "structure" :parent_concept structure-concept))
(define correspondence-concept
  (def-concept :name "correspondence" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define label-concept
  (def-concept :name "label" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define relation-concept
  (def-concept :name "relation" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define chunk-concept
  (def-concept :name "chunk" :locations (list (Location (list) structure-space))
    :parent_space structure-space
    :activation 1.0))
(define letter-chunk-concept
  (def-concept :name "letter-chunk" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define frame-concept
  (def-concept :name "frame" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define view-concept
  (def-concept :name "view" :locations (list (Location (list) structure-space))
    :parent_space structure-space))

(def-relation :start suggest-concept :end chunk-concept)
(def-relation :start suggest-concept :end correspondence-concept)
(def-relation :start suggest-concept :end frame-concept)
(def-relation :start suggest-concept :end label-concept)
(def-relation :start suggest-concept :end letter-chunk-concept)
(def-relation :start suggest-concept :end relation-concept)
(def-relation :start suggest-concept :end view-concept)

(def-relation :start build-concept :end chunk-concept)
(def-relation :start build-concept :end correspondence-concept)
(def-relation :start build-concept :end frame-concept)
(def-relation :start build-concept :end label-concept)
(def-relation :start build-concept :end letter-chunk-concept)
(def-relation :start build-concept :end relation-concept)
(def-relation :start build-concept :end view-concept)

(def-relation :start evaluate-concept :end chunk-concept)
(def-relation :start evaluate-concept :end correspondence-concept)
(def-relation :start evaluate-concept :end frame-concept)
(def-relation :start evaluate-concept :end label-concept)
(def-relation :start evaluate-concept :end letter-chunk-concept)
(def-relation :start evaluate-concept :end relation-concept)
(def-relation :start evaluate-concept :end view-concept)

(def-relation :start select-concept :end chunk-concept)
(def-relation :start select-concept :end correspondence-concept)
(def-relation :start select-concept :end frame-concept)
(def-relation :start select-concept :end label-concept)
(def-relation :start select-concept :end letter-chunk-concept)
(def-relation :start select-concept :end relation-concept)
(def-relation :start select-concept :end view-concept)

(def-relation :start inner-concept :end outer-concept)

(def-relation :start chunk-concept :end inner-concept)
(def-relation :start label-concept :end inner-concept)
(def-relation :start relation-concept :end inner-concept)

(def-relation :start chunk-concept :end outer-concept)
(def-relation :start letter-chunk-concept :end outer-concept)
(def-relation :start label-concept :end outer-concept)
(def-relation :start relation-concept :end outer-concept)

(def-relation :start suggest-concept :end build-concept :is_bidirectional False)
(def-relation :start build-concept :end evaluate-concept :is_bidirectional False)
(def-relation :start evaluate-concept :end select-concept :is_bidirectional False)
(def-relation :start select-concept :end suggest-concept :is_bidirectional False)

(def-relation :start chunk-concept :end label-concept
  :is_bidirectional False :activation 0.33)
(def-relation :start label-concept :end chunk-concept
  :is_bidirectional False :is_excitatory False :activation 1.0)

(def-relation :start label-concept :end relation-concept
  :is_bidirectional False :activation 0.33)
(def-relation :start relation-concept :end label-concept
  :is_bidirectional False :is_excitatory False :activation 1.0)

(def-relation :start relation-concept :end view-concept
  :is_bidirectional False :activation 0.33)
(def-relation :start view-concept :end relation-concept
  :is_bidirectional False :is_excitatory False :activation 1.0)

(def-relation :start relation-concept :end frame-concept
  :is_bidirectional False :activation 0.33)
(def-relation :start frame-concept :end relation-concept
  :is_bidirectional False :is_excitatory False :activation 1.0)

(def-relation :start view-concept :end correspondence-concept
  :is_bidirectional False :activation 0.33)
(def-relation :start correspondence-concept :end view-concept
  :is_bidirectional False :is_excitatory False :activation 1.0)

(def-relation :start correspondence-concept :end letter-chunk-concept
  :is_bidirectional False :activation 0.33)
(def-relation :start letter-chunk-concept :end correspondence-concept
  :is_bidirectional False :is_excitatory False :activation 1.0)

(def-relation :start letter-chunk-concept :end chunk-concept
  :is_bidirectional False :activation 0.33)
(def-relation :start chunk-concept :end letter-chunk-concept
  :is_bidirectional False :is_excitatory False :activation 1.0)

