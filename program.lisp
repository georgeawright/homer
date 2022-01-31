(define input-concept (def-concept :name "input"))
(define text-concept (def-concept :name "text"))

(define views-space
  (def-contextual-space :name "views" :parent_concept None
    :conceptual_spaces (StructureCollection)))

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
    :parent_space structure-space))
(define letter-chunk-concept
  (def-concept :name "letter-chunk" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define view-monitoring-concept
  (def-concept :name "view-monitoring" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define view-simplex-concept
  (def-concept :name "view-simplex" :locations (list (Location (list) structure-space))
    :parent_space structure-space))

(def-relation :start inner-concept :end chunk-concept :activation 1.0)
(def-relation :start chunk-concept :end label-concept :activation 1.0)
(def-relation :start chunk-concept :end relation-concept :activation 1.0)
(def-relation :start chunk-concept :end view-concept :activation 1.0)
(def-relation :start inner-concept :end label-concept :activation 1.0)
(def-relation :start inner-concept :end relation-concept :activation 1.0)
(def-relation :start view-concept :end view-simplex-concept :activation 1.0)
(def-relation :start view-concept :end view-monitoring-concept :activation 1.0)
(def-relation :start view-monitoring-concept :end reverse-concept :activation 1.0)
(def-relation :start view-monitoring-concept :end outer-concept :activation 1.0)
(def-relation :start reverse-concept :end outer-concept :activation 1.0)
(def-relation :start view-simplex-concept :end correspondence-concept :activation 1.0)
(def-relation :start view-simplex-concept :end letter-chunk-concept :activation 1.0)
(def-relation :start view-monitoring-concept :end letter-chunk-concept :activation 1.0)
(def-relation :start label-concept :end letter-chunk-concept :activation 1.0)
(def-relation :start relation-concept :end letter-chunk-concept :activation 1.0)
(def-relation :start view-monitoring-concept :end publish-concept :activation 1.0)

(def-relation :start suggest-concept :end build-concept
  :activation 1.0 :is_bidirectional False)
(def-relation :start build-concept :end evaluate-concept
  :activation 1.0 :is_bidirectional False)
(def-relation :start evaluate-concept :end select-concept
  :activation 1.0 :is_bidirectional False)
(def-relation :start select-concept :end suggest-concept
  :activation 1.0 :is_bidirectional False)

(def-relation :start suggest-concept :end correspondence-concept)
(def-relation :start suggest-concept :end label-concept :activation 1.0)
(def-relation :start suggest-concept :end relation-concept)
(def-relation :start suggest-concept :end chunk-concept)
(def-relation :start suggest-concept :end letter-chunk-concept)
(def-relation :start suggest-concept :end view-simplex-concept)
(def-relation :start suggest-concept :end view-monitoring-concept)
(def-relation :start build-concept :end correspondence-concept)
(def-relation :start build-concept :end label-concept :activation 1.0)
(def-relation :start build-concept :end relation-concept)
(def-relation :start build-concept :end chunk-concept)
(def-relation :start build-concept :end letter-chunk-concept)
(def-relation :start build-concept :end view-simplex-concept)
(def-relation :start build-concept :end view-monitoring-concept)
(def-relation :start evaluate-concept :end correspondence-concept)
(def-relation :start evaluate-concept :end label-concept :activation 1.0)
(def-relation :start evaluate-concept :end relation-concept)
(def-relation :start evaluate-concept :end chunk-concept)
(def-relation :start evaluate-concept :end letter-chunk-concept)
(def-relation :start evaluate-concept :end view-simplex-concept)
(def-relation :start evaluate-concept :end view-monitoring-concept)
(def-relation :start select-concept :end correspondence-concept)
(def-relation :start select-concept :end label-concept :activation 1.0)
(def-relation :start select-concept :end relation-concept)
(def-relation :start select-concept :end chunk-concept)
(def-relation :start select-concept :end letter-chunk-concept)
(def-relation :start select-concept :end view-simplex-concept)
(def-relation :start select-concept :end view-monitoring-concept)

(define grammar-distance-to-proximity 0.1)
(define grammar-concept (def-concept :name "grammar"))
(define grammar-space
  (def-conceptual-space :name "grammar" :parent_concept grammar-concept
    :no_of_dimensions 0))
(define sentence-concept
  (def-concept :name "sentence" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define np-concept
  (def-concept :name "np" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define vp-concept
  (def-concept :name "vp" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define ap-concept
  (def-concept :name "ap" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define rp-concept
  (def-concept :name "rp" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define pp-concept
  (def-concept :name "pp" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define nn-concept
  (def-concept :name "nn" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define vb-concept
  (def-concept :name "vb" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define jj-concept
  (def-concept :name "jj" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define jjr-concept
  (def-concept :name "jjr" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define rb-concept
  (def-concept :name "rb" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define cop-concept
  (def-concept :name "cop" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define prep-concept
  (def-concept :name "prep" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define det-concept
  (def-concept :name "det" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define conj-concept
  (def-concept :name "conj" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))

(define the (def-letter-chunk :name "the" :locations (list (Location (list) grammar-space))))
(define is (def-letter-chunk :name "is" :locations (list (Location (list) grammar-space))))
(define it (def-letter-chunk :name "it" :locations (list (Location (list) grammar-space))))
(define in (def-letter-chunk :name "in" :locations (list (Location (list) grammar-space))))
(define than (def-letter-chunk :name "than" :locations (list (Location (list) grammar-space))))
(define and (def-letter-chunk :name "and" :locations (list (Location (list) grammar-space))))
(define but (def-letter-chunk :name "but" :locations (list (Location (list) grammar-space))))
(define comma (def-letter-chunk :name "comma" :locations (list (Location (list) grammar-space))))
(define fstop (def-letter-chunk :name "fstop" :locations (list (Location (list) grammar-space))))
(define -er (def-letter-chunk :name "er" :locations (list (Location (list) grammar-space))))
(define null (def-letter-chunk :name "" :locations (list (Location (list) grammar-space))))

(define same-different-concept
  (def-concept :name "same-different" :locations (list) :classifier None :instance_type None
    :structure_type Correspondence :parent_space None
    :distance_function centroid_euclidean_distance))
(define same-different-space
  (def-conceptual-space :name "same-different" :parent_concept same-different-concept
    :no_of_dimensions 1))
(define same-concept
  (def-concept :name "same"
    :locations (list (Location (list (list 10)) same-different-space))
    :classifier (SamenessClassifier) :instance_type Chunk :structure_type Correspondence
    :parent_space same-different-space :distance_function centroid_euclidean_distance))
(define different-concept
  (def-concept :name "different"
    :locations (list (Location (list (list 10)) same-different-space))
    :classifier (DifferentnessClassifier) :instance_type Chunk :structure_type Correspondence
    :parent_space same-different-space :distance_function centroid_euclidean_distance))

(define sameness-rule
  (def-rule :name "same->same" :location (Location (list) same-different-space)
    :root_concept same-concept :left_concept same-concept :right_concept None))

(define same-word (def-letter-chunk :name "same" :locations (list)))
(def-relation :start same-concept :end same-word :parent_concept jj-concept)
(define different-word (def-letter-chunk :name "different" :locations (list)))
(def-relation :start different-concept :end different-word :parent_concept jj-concept)

(define more-less-concept
  (def-concept :name "more-less" :locations (list) :classifier None :instance_type None
    :structure_type None :parent_space None
    :distance_function centroid_euclidean_distance))
(define more-less-space
  (def-conceptual-space :name "more-less" :parent_concept more-less-concept
    :no_of_dimensions 1))
(define more-concept
  (def-concept :name "more" :locations (list (Location (list (list 5)) more-less-space))
    :classifier (DifferenceClassifier 5) :instance_type Chunk :structure_type Relation
    :parent_space more-less-space :distance_function centroid_euclidean_distance))
(define less-concept
  (def-concept :name "less" :locations (list (Location (list (list -5)) more-less-space))
    :classifier (DifferenceClassifier -5) :instance_type Chunk :structure_type Relation
    :parent_space more-less-space :distance_function centroid_euclidean_distance))

(define more-word (def-letter-chunk :name "more" :locations (list)))
(def-relation :start more-concept :end more-word :parent_concept jj-concept)
(define less-word (def-letter-chunk :name "less" :locations (list)))
(def-relation :start less-concept :end less-word :parent_concept jj-concept)

(define magnitude-concept
  (def-concept :name "magnitude" :locations (list) :classifier None :instance_type None
    :structure_type None :parent_space None
    :distance_function centroid_euclidean_distance))
(define magnitude-space
  (def-conceptual-space :name "magnitude" :parent_concept magnitude-concept
    :no_of_dimensions 1))
(define extremely-concept
  (def-concept :name "extremely"
    :locations (list (Location (list (list 2)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Label :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))
(define very-concept
  (def-concept :name "very"
    :locations (list (Location (list (list 1)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Label :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))
(define quite-concept
  (def-concept :name "quite"
    :locations (list (Location (list (list -1)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Label :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))
(define bit-concept
  (def-concept :name "bit"
    :locations (list (Location (list (list -2)) magnitude-space))
    :classifier (ProximityClassifier) :instance_type Label :structure_type Label
    :parent_space magnitude-space :distance_function centroid_euclidean_distance))

(define extremely-word (def-letter-chunk :name "extremely" :locations (list)))
(def-relation :start extremely-concept :end extremely-word :parent_concept rb-concept)
(define very-word (def-letter-chunk :name "very" :locations (list)))
(def-relation :start very-concept :end very-word :parent_concept rb-concept)
(define quite-word (def-letter-chunk :name "quite" :locations (list)))
(def-relation :start quite-concept :end quite-word :parent_concept rb-concept)
(define bit-word (def-letter-chunk :name "a bit" :locations (list)))
(def-relation :start bit-concept :end bit-word :parent_concept rb-concept)

(define height-concept
  (def-concept :name "height" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define height-space
  (def-conceptual-space :name "height" :parent_concept height-concept
    :no_of_dimensions 1 :is_basic_level True))
(define high-concept
  (def-concept :name "high" :locations (list (Location (list (list 10)) height-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space height-space :distance_function centroid_euclidean_distance))
(define low-concept
  (def-concept :name "low" :locations (list (Location (list (list 0)) height-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space height-space :distance_function centroid_euclidean_distance))

(define high-word (def-letter-chunk :name "high" :locations (list)))
(def-relation :start high-concept :end high-word :parent_concept jj-concept)
(def-relation :start high-concept :end high-word :parent_concept jjr-concept)
(def-relation :start high-word :end -er :parent_concept jjr-concept)
(define low-word (def-letter-chunk :name "low" :locations (list)))
(def-relation :start low-concept :end low-word :parent_concept jj-concept)
(def-relation :start low-concept :end low-word :parent_concept jjr-concept)
(def-relation :start low-word :end -er :parent_concept jjr-concept)

(define goodness-concept
  (def-concept :name "goodness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define goodness-space
  (def-conceptual-space :name "goodness" :parent_concept goodness-concept
    :no_of_dimensions 1 :is_basic_level True))
(define good-concept
  (def-concept :name "good" :locations (list (Location (list (list 10)) goodness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space goodness-space :distance_function centroid_euclidean_distance))
(define bad-concept
  (def-concept :name "bad" :locations (list (Location (list (list 0)) goodness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space goodness-space :distance_function centroid_euclidean_distance))

(define good-word (def-letter-chunk :name "good" :locations (list)))
(def-relation :start good-concept :end good-word :parent_concept jj-concept)
(define bett-word (def-letter-chunk :name "bett" :locations (list)))
(def-relation :start good-concept :end bett-word :parent_concept jjr-concept)
(def-relation :start bett-word :end -er :parent_concept jjr-concept)
(define bad-word (def-letter-chunk :name "bad" :locations (list)))
(def-relation :start bad-concept :end bad-word :parent_concept jj-concept)
(define worse-word (def-letter-chunk :name "worse" :locations (list)))
(def-relation :start bad-concept :end worse-word :parent_concept jjr-concept)
(def-relation :start worse-word :end null :parent_concept jjr-concept)

(define extremeness-concept
  (def-concept :name "extremeness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define extremeness-space
  (def-conceptual-space :name "extremeness" :parent_concept extremeness-concept
    :no_of_dimensions 1))
(define extreme-concept
  (def-concept :name "extreme" :locations (list (Location (list (list 10)) extremeness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space extremeness-space :distance_function centroid_euclidean_distance))

(define extreme-word (def-letter-chunk :name "extreme" :locations (list)))
(def-relation :start extreme-concept :end extreme-word :parent_concept jj-concept)

(define temperature-concept
  (def-concept :name "temperature" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define temperature-space
  (def-conceptual-space :name "temperature" :parent_concept temperature-concept
    :no_of_dimensions 1 :is_basic_level True))
(define hot-concept
  (def-concept :name "hot" :locations (list (Location (list (list 22)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance))
(define warm-concept
  (def-concept :name "warm" :locations (list (Location (list (list 18)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance))
(define mild-concept
  (def-concept :name "mild"
    :locations (list (Location (list (list 0)) extremeness-space)
		     (Location (list (list 13)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space extremeness-space :distance_function centroid_euclidean_distance))
(define cool-concept
  (def-concept :name "cool" :locations (list (Location (list (list 8)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance))
(define cold-concept
  (def-concept :name "cold" :locations (list (Location (list (list 4)) temperature-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space temperature-space :distance_function centroid_euclidean_distance))

(define hot-word (def-letter-chunk :name "hot" :locations (list)))
(def-relation :start hot-concept :end hot-word :parent_concept jj-concept)
(define hott-word (def-letter-chunk :name "hott" :locations (list)))
(def-relation :start hot-concept :end hott-word :parent_concept jjr-concept)
(def-relation :start hott-word :end -er :parent_concept jjr-concept)
(define heat-word (def-letter-chunk :name "heat" :locations (list)))
(def-relation :start hot-concept :end heat-word :parent_concept nn-concept)
(define warm-word (def-letter-chunk :name "warm" :locations (list)))
(def-relation :start warm-concept :end warm-word :parent_concept jj-concept)
(def-relation :start warm-concept :end warm-word :parent_concept jjr-concept)
(def-relation :start warm-word :end -er :parent_concept jjr-concept)
(define warmth-word (def-letter-chunk :name "warmth" :locations (list)))
(def-relation :start warm-concept :end warmth-word :parent_concept nn-concept)
(define mild-word (def-letter-chunk :name "mild" :locations (list)))
(def-relation :start mild-concept :end mild-word :parent_concept jj-concept)
(def-relation :start mild-concept :end mild-word :parent_concept jjr-concept)
(def-relation :start mild-word :end -er :parent_concept jjr-concept)
(define cool-word (def-letter-chunk :name "cool" :locations (list)))
(def-relation :start cool-concept :end cool-word :parent_concept jj-concept)
(def-relation :start cool-concept :end cool-word :parent_concept jjr-concept)
(def-relation :start cool-word :end -er :parent_concept jjr-concept)
(define cold-word (def-letter-chunk :name "cold" :locations (list)))
(def-relation :start cold-concept :end cold-word :parent_concept jj-concept)
(def-relation :start cold-concept :end cold-word :parent_concept jjr-concept)
(def-relation :start cold-word :end -er :parent_concept jjr-concept)

(define peripheralness-concept
  (def-concept :name "peripheralness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define peripheralness-space
  (def-conceptual-space :name "peripheralness" :parent_concept peripheralness-concept
    :no_of_dimensions 1))
(define peripheral-concept
  (def-concept :name "peripheral"
    :locations (list (Location (list (list 10)) peripheralness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space peripheralness-space :distance_function centroid_euclidean_distance))

(define peripheries-word (def-letter-chunk :name "peripheries" :locations (list)))
(def-relation :start peripheral-concept :end peripheries-word :parent_concept nn-concept)

(define location-concept
  (def-concept :name "location" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define north-south-space
  (def-conceptual-space :name "north-south" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[c[0]] for c in location.coordinates]
"""))))))
(define west-east-space
  (def-conceptual-space :name "west-east" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[c[1]] for c in location.coordinates]
"""))))))
(define nw-se-space
  (def-conceptual-space :name "northwest-southeast" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[sum(c)/len(c)] for c in location.coordinates]
"""))))))
(define ne-sw-space
  (def-conceptual-space :name "northeast-southwest" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python """
lambda location: [[(c[0]+4-c[1])/2] for c in location.coordinates]
"""))))))
(define location-space
  (def-conceptual-space :name "location" :parent_concept location-concept
    :no_of_dimensions 2
    :dimensions (list north-south-space west-east-space)
    :sub_spaces (list north-south-space west-east-space nw-se-space ne-sw-space)
    :is_basic_level True))
(define north-concept
  (def-concept :name "north" :locations (list (Location (list (list 0 4)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define south-concept
  (def-concept :name "south" :locations (list (Location (list (list 10 4)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define west-concept
  (def-concept :name "west" :locations (list (Location (list (list 5 0)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define east-concept
  (def-concept :name "east" :locations (list (Location (list (list 5 8)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define northwest-concept
  (def-concept :name "northwest" :locations (list (Location (list (list 0 0)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define northeast-concept
  (def-concept :name "northeast" :locations (list (Location (list (list 0 8)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define southwest-concept
  (def-concept :name "southwest" :locations (list (Location (list (list 10 0)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define southeast-concept
  (def-concept :name "southeast" :locations (list (Location (list (list 10 8)) location-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))
(define central-concept
  (def-concept :name "central"
    :locations (list (Location (list (list 5 4)) location-space)
		     (Location (list (list 0)) peripheralness-space))
    :classifier (ProximityClassifier) :instance_type Chunk :structure_type Label
    :parent_space location-space :distance_function centroid_euclidean_distance))

(define north-word (def-letter-chunk :name "north" :locations (list)))
(def-relation :start north-concept :end north-word :parent_concept nn-concept)
(define south-word (def-letter-chunk :name "south" :locations (list)))
(def-relation :start south-concept :end south-word :parent_concept nn-concept)
(define west-word (def-letter-chunk :name "west" :locations (list)))
(def-relation :start west-concept :end west-word :parent_concept nn-concept)
(define east-word (def-letter-chunk :name "east" :locations (list)))
(def-relation :start east-concept :end east-word :parent_concept nn-concept)
(define northwest-word (def-letter-chunk :name "northwest" :locations (list)))
(def-relation :start northwest-concept :end northwest-word :parent_concept nn-concept)
(define northeast-word (def-letter-chunk :name "northeast" :locations (list)))
(def-relation :start northeast-concept :end northeast-word :parent_concept nn-concept)
(define southwest-word (def-letter-chunk :name "southwest" :locations (list)))
(def-relation :start southwest-concept :end southwest-word :parent_concept nn-concept)
(define southeast-word (def-letter-chunk :name "southeast" :locations (list)))
(def-relation :start southeast-concept :end southeast-word :parent_concept nn-concept)
(define centre-word (def-letter-chunk :name "centre" :locations (list)))
(def-relation :start central-concept :end centre-word :parent_concept nn-concept)
(define midlands-word (def-letter-chunk :name "midlands" :locations (list)))
(def-relation :start central-concept :end midlands-word :parent_concept nn-concept)

(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :no_of_dimensions Nan))
(define label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define nn-input
  (def-contextual-space :name "np[nn].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define nn-output
  (def-contextual-space :name "np[nn].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define nn-frame
  (def-frame :name "np[nn]"
    :parent_concept np-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection space-parent-concept label-concept)
    :input_space nn-input :output_space nn-output))
(define chunk
  (def-chunk :locations (list (Location (list) conceptual-space)
			      (Location (list) nn-input))
    :parent_space nn-input))
(define chunk-label
  (def-label :start chunk :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) nn-input))))
(define letter-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) nn-output))))
(define letter-chunk-grammar-label
  (def-label :start letter-chunk :parent_concept nn-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) nn-input))))
(define letter-chunk-meaning-label
  (def-label :start letter-chunk :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) nn-input))))

(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :no_of_dimensions 1))
(define label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define relation-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space))
(def-relation :start label-concept :end relation-concept
  :parent_concept more-concept)
(define rp-input
  (def-contextual-space :name "rp[jjr].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define rp-output
  (def-contextual-space :name "rp[jjr].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define rp-frame
  (def-frame :name "rp[jjr]"
    :parent_concept rp-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection space-parent-concept label-concept relation-concept)
    :input_space rp-input :output_space rp-output))
(define chunk-start
  (def-chunk :locations (list (Location (list) conceptual-space)
			      (Location (list) rp-input))
    :parent_space nn-input))
(define chunk-end
  (def-chunk :locations (list (Location (list) conceptual-space)
			      (Location (list) rp-input))
    :parent_space nn-input))
(define chunk-end-label
  (def-label :start chunk-end :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) rp-input))))
(define relation
  (def-relation :start chunk-start :end chunk-end :parent_concept relation-concept
    :locations (list (Location (list Nan) more-less-space)
		     (TwoPointLocation (list) (list) conceptual-space)
		     (TwoPointLocation (list) (list) rp-input))
    :conceptual_space conceptual-space))
(define jjr-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) rp-output))))
(define er-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) rp-output))))
(define jjr-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) rp-output))
    :left_branch (StructureCollection jjr-chunk)
    :right_branch (StructureCollection er-chunk)))
(define jjr-chunk-grammar-label
  (def-label :start jjr-chunk :parent_concept jjr-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-input))))
(define jjr-chunk-meaning-label
  (def-label :start jjr-chunk :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) rp-input))))
(define er-chunk-relation
  (def-relation :start jjr-chunk :end er-chunk :parent_concept jjr-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-input))))



(define input-space
  (def-contextual-space :name "input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection temperature-space location-space)))

(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0 0)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0 1)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0 2)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0 3)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0 4)) location-space))
  :parent_space input-space)

(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 1 0)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 1 1)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 1 2)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 1 3)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 1 4)) location-space))
  :parent_space input-space)

(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 2 0)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 2 1)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 2 3)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)

(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 3 0)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 3 1)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 3 2)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 3 3)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 3 4)) location-space))
  :parent_space input-space)

(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 4 0)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 4 1)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 4 3)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)

(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 5 0)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 5 1)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 5 2)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 5 3)) location-space))
  :parent_space input-space)
(def-chunk
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 5 4)) location-space))
  :parent_space input-space)
