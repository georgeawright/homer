import pytest
import sys
from unittest.mock import Mock

from linguoplotter import Linguoplotter
from linguoplotter.loggers import ActivityLogger


@pytest.fixture(scope="module")
def program():
    return """
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
(define space-conceptual-concept
  (def-concept :name "space-conceptual" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define view-monitoring-concept
  (def-concept :name "view-monitoring" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
(define view-simplex-concept
  (def-concept :name "view-simplex" :locations (list (Location (list) structure-space))
    :parent_space structure-space))
    
(def-relation :start suggest-concept :end chunk-concept)
(def-relation :start suggest-concept :end correspondence-concept)
(def-relation :start suggest-concept :end label-concept)
(def-relation :start suggest-concept :end letter-chunk-concept)
(def-relation :start suggest-concept :end relation-concept)
(def-relation :start suggest-concept :end view-simplex-concept)

(def-relation :start build-concept :end chunk-concept)
(def-relation :start build-concept :end correspondence-concept)
(def-relation :start build-concept :end label-concept)
(def-relation :start build-concept :end letter-chunk-concept)
(def-relation :start build-concept :end relation-concept)
(def-relation :start build-concept :end view-simplex-concept)

(def-relation :start evaluate-concept :end chunk-concept)
(def-relation :start evaluate-concept :end correspondence-concept)
(def-relation :start evaluate-concept :end label-concept)
(def-relation :start evaluate-concept :end letter-chunk-concept)
(def-relation :start evaluate-concept :end relation-concept)
(def-relation :start evaluate-concept :end view-simplex-concept)

(def-relation :start select-concept :end chunk-concept)
(def-relation :start select-concept :end correspondence-concept)
(def-relation :start select-concept :end label-concept)
(def-relation :start select-concept :end letter-chunk-concept)
(def-relation :start select-concept :end relation-concept)
(def-relation :start select-concept :end view-simplex-concept)

(define grammar-distance-to-proximity 0.1)
(define grammar-concept
  (def-concept :name "grammar" :distance_function centroid_euclidean_distance))
(define grammar-space
  (def-conceptual-space :name "grammar" :parent_concept grammar-concept
    :no_of_dimensions 0 :is_basic_level True))
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
(define nsubj-concept
  (def-concept :name "nsubj" :locations (list (Location (list (list)) grammar-space))
    :instance_type LetterChunk :structure_type Label :parent_space grammar-space
    :distance_function centroid_euclidean_distance
    :distance_to_proximity_weight grammar-distance-to-proximity))
(define predicate-concept
  (def-concept :name "predicate" :locations (list (Location (list (list)) grammar-space))
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
(define will (def-letter-chunk :name "will" :locations (list (Location (list) grammar-space))))
(define be (def-letter-chunk :name "be" :locations (list (Location (list) grammar-space))))
(define temperatures (def-letter-chunk :name "temperatures" :locations (list (Location (list) grammar-space))))
(define in (def-letter-chunk :name "in" :locations (list (Location (list) grammar-space))))
(define than (def-letter-chunk :name "than" :locations (list (Location (list) grammar-space))))
(define and (def-letter-chunk :name "and" :locations (list (Location (list) grammar-space))))
(define but (def-letter-chunk :name "but" :locations (list (Location (list) grammar-space))))
(define comma (def-letter-chunk :name "comma" :locations (list (Location (list) grammar-space))))
(define fstop (def-letter-chunk :name "fstop" :locations (list (Location (list) grammar-space))))
(define -er (def-letter-chunk :name "\ber" :locations (list (Location (list) grammar-space))))
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
  (def-concept :name "more-less" :locations (list) :classifier None :instance_type Chunk
    :structure_type Relation :parent_space None
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
    
(def-relation :start more-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start less-concept :end less-concept :parent_concept more-concept :activation 1.0)

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
    :no_of_dimensions 1 :is_basic_level True))
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
(define bit-word (def-letter-chunk :name \"""a bit\""" :locations (list)))
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

(def-relation :start high-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start low-concept :end less-concept :parent_concept more-concept :activation 1.0)

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

(def-relation :start good-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start bad-concept :end less-concept :parent_concept more-concept :activation 1.0)

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
    :locations (list
		(Location (list (list 0)) extremeness-space)
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
    
(def-relation :start hot-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start warm-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start extreme-concept :end more-concept :parent_concept more-concept :activation 1.0)
(def-relation :start cool-concept :end less-concept :parent_concept more-concept :activation 1.0)
(def-relation :start cold-concept :end less-concept :parent_concept more-concept :activation 1.0)
(def-relation :start mild-concept :end less-concept :parent_concept more-concept :activation 1.0)

(def-correspondence :start hot-concept :end high-concept :parent_concept same-concept)
(def-correspondence :start hot-concept :end good-concept :parent_concept same-concept)
(def-correspondence :start cold-concept :end low-concept :parent_concept same-concept)
(def-correspondence :start cold-concept :end bad-concept :parent_concept same-concept)
   
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
(define cold-word (def-letter-chunk :name "cold" :locations (list (Location (list) grammar-space) (Location (list (list 4)) temperature-space))))
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
    (dict (list (tuple "location" (python \"""
lambda location: [[c[0]] for c in location.coordinates]
\"""))))))
(define west-east-space
  (def-conceptual-space :name "west-east" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python \"""
lambda location: [[c[1]] for c in location.coordinates]
\"""))))))
(define nw-se-space
  (def-conceptual-space :name "northwest-southeast" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python \"""
lambda location: [[sum(c)/len(c)] for c in location.coordinates]
\"""))))))
(define ne-sw-space
  (def-conceptual-space :name "northeast-southwest" :parent_concept location-concept
    :no_of_dimensions 1
    :super_space_to_coordinate_function_map
    (dict (list (tuple "location" (python \"""
lambda location: [[(c[0]+4-c[1])/2] for c in location.coordinates]
\"""))))))
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

(define north-word
  (def-letter-chunk :name "north"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 0 4)) location-space))))
(def-relation :start north-concept :end north-word :parent_concept nn-concept)
(define south-word
  (def-letter-chunk :name "south"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 10 4)) location-space))))
(def-relation :start south-concept :end south-word :parent_concept nn-concept)
(define west-word
  (def-letter-chunk :name "west"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 5 0)) location-space))))
(def-relation :start west-concept :end west-word :parent_concept nn-concept)
(define east-word
  (def-letter-chunk :name "east"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 5 8)) location-space))))
(def-relation :start east-concept :end east-word :parent_concept nn-concept)
(define northwest-word
  (def-letter-chunk :name "northwest"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 0 0)) location-space))))
(def-relation :start northwest-concept :end northwest-word :parent_concept nn-concept)
(define northeast-word
  (def-letter-chunk :name "northeast"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 0 8)) location-space))))
(def-relation :start northeast-concept :end northeast-word :parent_concept nn-concept)
(define southwest-word
  (def-letter-chunk :name "southwest"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 10 0)) location-space))))
(def-relation :start southwest-concept :end southwest-word :parent_concept nn-concept)
(define southeast-word
  (def-letter-chunk :name "southeast"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 10 8)) location-space))))
(def-relation :start southeast-concept :end southeast-word :parent_concept nn-concept)
(define centre-word
  (def-letter-chunk :name "centre"
    :locations (list (Location (list) grammar-space))))
(def-relation :start central-concept :end centre-word :parent_concept nn-concept)
(define midlands-word
  (def-letter-chunk :name "midlands"
    :locations (list (Location (list) grammar-space)
		     (Location (list (list 5 4)) location-space)
		     (Location (list (list 0)) peripheralness-space))))
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
    :no_of_dimensions Nan))
(define label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define jj-input
  (def-contextual-space :name "ap[jj].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define jj-output
  (def-contextual-space :name "ap[jj].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define jj-frame
  (def-frame :name "ap[jj]"
    :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection space-parent-concept label-concept)
    :input_space jj-input :output_space jj-output))
(define chunk
  (def-chunk :locations (list (Location (list) conceptual-space)
			      (Location (list) jj-input))
    :parent_space jj-input))
(define chunk-label
  (def-label :start chunk :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) jj-input))))
(define letter-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) jj-output))))
(define letter-chunk-grammar-label
  (def-label :start letter-chunk :parent_concept jj-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) jj-input))))
(define letter-chunk-meaning-label
  (def-label :start letter-chunk :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) jj-input))))

(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :no_of_dimensions Nan))
(define magnitude-label-concept
  (def-concept :name "" :is_slot True :parent_space magnitude-space))
(define label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define ap-sub-frame-input
  (def-contextual-space :name "ap-ap-sub.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define ap-sub-frame-output
  (def-contextual-space :name "ap-ap-sub.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define ap-sub-frame
  (def-frame  :name "ap-ap-sub" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space ap-sub-frame-input
    :output_space ap-sub-frame-output))
(define ap-frame-input
  (def-contextual-space :name "ap-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection magnitude-space conceptual-space)))
(define ap-frame-output
  (def-contextual-space :name "ap-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space magnitude-space conceptual-space)))
(define ap-frame
  (def-frame :name "ap-frame" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection ap-sub-frame)
    :concepts (StructureCollection magnitude-label-concept)
    :input_space ap-frame-input
    :output_space ap-frame-output))
(define label-start
  (def-link-or-node :locations (list (Location (list (list Nan)) conceptual-space)
				     (Location (list) ap-frame-input))
    :parent_space ap-frame-input))
(define label-start-label
  (def-label :start label-start :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list (list Nan)) magnitude-space)
		     (Location (list) ap-frame-input))))
(define magnitude-label
  (def-label :start label-start-label :parent_concept magnitude-label-concept
    :locations (list (Location (list (list Nan)) magnitude-space)
		     (Location (list) ap-frame-input))))
(define qualifier-word
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) ap-frame-output))
    :parent_space ap-frame-output))
(define qualifier-word-grammar-label
  (def-label :start qualifier-word :parent_concept rb-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) ap-frame-output))))
(define qualifier-word-magnitude-label
  (def-label :start qualifier-word :parent_concept magnitude-label-concept
    :locations (list (Location (list) magnitude-space)
		     (Location (list) ap-frame-output))))
(define adjective-word
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) ap-sub-frame-output)
		     (Location (list) ap-frame-output))
    :parent_space ap-sub-frame-output))
(define adjective-word-grammar-label
  (def-label :start adjective-word :parent_concept jj-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) ap-sub-frame-output)
		     (Location (list) ap-frame-output))))
(define adjectival-phrase
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) ap-frame-output))
    :left_branch (StructureCollection qualifier-word)
    :right_branch (StructureCollection adjective-word)
    :parent_space ap-sub-frame-output))

(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :no_of_dimensions 1))
(define label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space
    :locations (list (Location (list) conceptual-space))))
(define relation-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(def-relation :start label-concept :end relation-concept
  :parent_concept more-concept :activation 1.0)
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
    :parent_space rp-input))
(define chunk-end
  (def-chunk :locations (list (Location (list) conceptual-space)
			      (Location (list) rp-input))
    :parent_space rp-input))
(define chunk-start-label
  (def-label :start chunk-start :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) rp-input))))
(define relation
  (def-relation :start chunk-start :end chunk-end :parent_concept relation-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list) (list) conceptual-space)
		     (TwoPointLocation (list) (list) rp-input))
    :conceptual_space conceptual-space))
(define jjr-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) rp-output))
    :parent_space rp-output))
(define er-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) rp-output))
     :parent_space rp-output))
(define jjr-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) conceptual-space)
		     (Location (list) grammar-space)
		     (Location (list) rp-output))
    :parent_space rp-output
    :left_branch (StructureCollection jjr-chunk)
    :right_branch (StructureCollection er-chunk)))
(define jjr-chunk-grammar-label
  (def-label :start jjr-chunk :parent_concept jjr-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-output))))
(define jjr-chunk-meaning-label
  (def-label :start jjr-chunk :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) rp-output))))
(define er-chunk-relation
  (def-relation :start jjr-chunk :end er-chunk :parent_concept jjr-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-output))))
(define jjr-super-chunk-label
  (def-label :start jjr-super-chunk :parent_concept jjr-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-output))))

(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :no_of_dimensions 1))
(define label-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space
    :locations (list (Location (list) conceptual-space))))
(define location-concept-1
  (def-concept :name "" :is_slot True :parent_space location-space))
(define location-concept-2
  (def-concept :name "" :is_slot True :parent_space location-space))
(define relation-concept
  (def-concept :name "" :is_slot True :parent_space more-less-space
    :locations (list (Location (list) more-less-space))))
(def-relation :start label-concept :end relation-concept
  :parent_concept more-concept :activation 1.0)
(define rp-sub-frame-input
  (def-contextual-space :name "rp-sub-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space conceptual-space)))
(define rp-sub-frame-output
  (def-contextual-space :name "rp-sub-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection
			grammar-space location-space conceptual-space)))
(define rp-sub-frame
  (def-frame :name "s-comparative-rp-sub" :parent_concept rp-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection label-concept relation-concept)
    :input_space rp-sub-frame-input
    :output_space rp-sub-frame-output))
(define nn-sub-frame-1-input
  (def-contextual-space :name "nn-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space conceptual-space)))
(define nn-sub-frame-1-output
  (def-contextual-space :name "nn-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection
			grammar-space location-space conceptual-space)))
(define nn-sub-frame-1
  (def-frame :name "s-comparative-nn-sub-1" :parent_concept np-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection location-concept-1)
    :input_space nn-sub-frame-1-input
    :output_space nn-sub-frame-1-output))
(define nn-sub-frame-2-input
  (def-contextual-space :name "nn-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space conceptual-space)))
(define nn-sub-frame-2-output
  (def-contextual-space :name "nn-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection
			grammar-space location-space conceptual-space)))
(define nn-sub-frame-2
  (def-frame :name "s-comparative-nn-sub-2" :parent_concept np-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection location-concept-2)
    :input_space nn-sub-frame-2-input
    :output_space nn-sub-frame-2-output))
(define comparative-sentence-input
  (def-contextual-space :name "s-comparative.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space conceptual-space)))
(define comparative-sentence-output
  (def-contextual-space :name "s-comparative.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection
			grammar-space location-space conceptual-space)))
(define comparative-sentence
  (def-frame :name "s-comparative" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection rp-sub-frame nn-sub-frame-1 nn-sub-frame-2)
    :concepts (StructureCollection
	       label-concept relation-concept location-concept-1 location-concept-2)
    :input_space comparative-sentence-input
    :output_space comparative-sentence-output))
 (define chunk-start
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) conceptual-space)
			      (Location (list) nn-sub-frame-1-input)
			      (Location (list) rp-sub-frame-input)
			      (Location (list) comparative-sentence-input))
    :parent_space nn-sub-frame-1-input))
(define chunk-end
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) conceptual-space)
			      (Location (list) nn-sub-frame-2-input)
			      (Location (list) rp-sub-frame-input)
			      (Location (list) comparative-sentence-input))
    :parent_space nn-sub-frame-2-input))
(define chunk-start-conceptual-label
  (def-label :start chunk-start :parent_concept label-concept
    :locations (list (Location (list) conceptual-space)
		     (Location (list) rp-sub-frame-input)
		     (Location (list) comparative-sentence-input))))
(define chunk-start-location-label
  (def-label :start chunk-start :parent_concept location-concept-1
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-1-input)
		     (Location (list) comparative-sentence-input))))
(define chunk-end-location-label
  (def-label :start chunk-end :parent_concept location-concept-2
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-2-input)
		     (Location (list) comparative-sentence-input))))
(define relation
  (def-relation :start chunk-start :end chunk-end :parent_concept relation-concept
    :locations (list (Location (list (list Nan)) more-less-space)
		     (TwoPointLocation (list) (list) conceptual-space)
		     (TwoPointLocation (list) (list) rp-sub-frame-input)
		     (TwoPointLocation (list) (list) comparative-sentence-input))
    :conceptual_space conceptual-space))
(define sentence-word-1
  (def-letter-chunk :name "temperatures"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk temperatures))
(define sentence-word-1-label
  (def-label :start sentence-word-1 :parent_concept nsubj-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))))
(define sentence-word-2
  (def-letter-chunk :name "will"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk will))
(define sentence-word-3
  (def-letter-chunk :name "be"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk be))
(define sentence-word-4
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-sub-frame-output)
		     (Location (list) comparative-sentence-output))
    :parent_space rp-sub-frame-output))
(define jjr-chunk-grammar-label
  (def-label :start sentence-word-4 :parent_concept jjr-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) rp-sub-frame-output))))
(define sentence-word-5
  (def-letter-chunk :name "in"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk in))
(define sentence-word-6
  (def-letter-chunk :name "the"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :parent_space comparative-sentence-output
    :abstract_chunk the))
(define sentence-word-7
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-1-output)
		     (Location (list) comparative-sentence-output))
    :parent_space nn-sub-frame-1-output))
(define nn-1-grammar-label
  (def-label :start sentence-word-7 :parent_concept np-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) nn-sub-frame-1-output))))
(define sentence-word-8
  (def-letter-chunk :name "than"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :abstract_chunk than))
(define sentence-word-9
  (def-letter-chunk :name "in"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :abstract_chunk in))
(define sentence-word-10
  (def-letter-chunk :name "the"
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :abstract_chunk the))
(define sentence-word-11
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) nn-sub-frame-2-output)
		     (Location (list) comparative-sentence-output))
    :parent_space nn-sub-frame-2-output))
(define nn-2-chunk-grammar-label
  (def-label :start sentence-word-11 :parent_concept np-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) nn-sub-frame-2-output))))
(define vb-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-2)
    :right_branch (StructureCollection sentence-word-3)))
(define vb-super-chunk-label
  (def-label :start vb-super-chunk :parent_concept vb-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))))
(define np-1-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-6)
    :right_branch (StructureCollection sentence-word-7)))
(define np-2-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-10)
    :right_branch (StructureCollection sentence-word-11)))
(define pp-1-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-5)
    :right_branch (StructureCollection np-1-super-chunk)))
(define pp-2-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-9)
    :right_branch (StructureCollection np-2-super-chunk)))
(define rp-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-4)
    :right_branch (StructureCollection pp-1-super-chunk)))
(define comp-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-8)
    :right_branch (StructureCollection pp-2-super-chunk)))
(define pred-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection rp-super-chunk)
    :right_branch (StructureCollection comp-super-chunk)))
(define pred-super-chunk-label
   (def-label :start pred-super-chunk :parent_concept predicate-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))))
(define vp-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection vb-super-chunk)
    :right_branch (StructureCollection pred-super-chunk)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))
    :left_branch (StructureCollection sentence-word-1)
    :right_branch (StructureCollection vp-super-chunk)))
(define sentence-super-chunk-label
  (def-label :start sentence-super-chunk :parent_concept sentence-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) comparative-sentence-output))))

(define and-sub-frame-1-input
  (def-contextual-space :name "and-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection)))
(define and-sub-frame-1-output
  (def-contextual-space :name "and-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space)))
(define and-sub-frame-1
  (def-frame :name "s-and-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space and-sub-frame-1-input
    :output_space and-sub-frame-1-output))
(define and-sub-frame-2-input
  (def-contextual-space :name "and-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection)))
(define and-sub-frame-2-output
  (def-contextual-space :name "and-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space)))
(define and-sub-frame-2
  (def-frame :name "s-and-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space and-sub-frame-2-input
    :output_space and-sub-frame-2-output))

(define and-sentence-input
  (def-contextual-space :name "s-and.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection)))
(define and-sentence-output
  (def-contextual-space :name "s-and.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space)))
(define and-sentence
  (def-frame :name "s-and" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection and-sub-frame-1 and-sub-frame-2)
    :concepts (StructureCollection)
    :input_space and-sentence-input
    :output_space and-sentence-output))

(define s-and-subject-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :parent_space and-sub-frame-1-output))
(define s-and-subject-1-grammar-label
  (def-label :start s-and-subject-1 :parent_concept nsubj-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-1-output))))
(define s-and-verb-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :parent_space and-sub-frame-1-output))
(define s-and-verb-1-grammar-label
  (def-label :start s-and-verb-1 :parent_concept vb-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-1-output))))
(define s-and-predicate-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :parent_space and-sub-frame-1-output))
(define s-and-predicate-1-grammar-label
  (def-label :start s-and-predicate-1 :parent_concept predicate-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-1-output))))
(define s-and-vp-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :left_branch (StructureCollection s-and-verb-1)
    :right_branch (StructureCollection s-and-predicate-1)
    :parent_space and-sub-frame-1-output))
(define s-and-vp-1-grammar-label
  (def-label :start s-and-vp-1 :parent_concept vp-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-1-output))))
(define s-and-clause-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-1-output))
    :left_branch (StructureCollection s-and-subject-1)
    :right_branch (StructureCollection s-and-vp-1)
    :parent_space and-sub-frame-1-output))
(define s-and-clause-1-grammar-label
  (def-label :start s-and-clause-1 :parent_concept sentence-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-1-output))))

(define s-and
  (def-letter-chunk :name "and"
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output))
    :parent_space and-sentence-output
    :abstract_chunk and))

(define s-and-subject-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :parent_space and-sub-frame-2-output))
(define s-and-subject-2-grammar-label
  (def-label :start s-and-subject-2 :parent_concept nsubj-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-2-output))))
(define s-and-verb-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :parent_space and-sub-frame-2-output))
(define s-and-verb-2-grammar-label
  (def-label :start s-and-verb-2 :parent_concept vb-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-2-output))))
(define s-and-predicate-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :parent_space and-sub-frame-2-output))
(define s-and-predicate-2-grammar-label
  (def-label :start s-and-predicate-2 :parent_concept predicate-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-2-output))))
(define s-and-vp-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :left_branch (StructureCollection s-and-verb-2)
    :right_branch (StructureCollection s-and-predicate-2)
    :parent_space and-sub-frame-2-output))
(define s-and-vp-2-grammar-label
  (def-label :start s-and-vp-2 :parent_concept vp-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-2-output))))
(define s-and-clause-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output)
		     (Location (list) and-sub-frame-2-output))
    :left_branch (StructureCollection s-and-subject-2)
    :right_branch (StructureCollection s-and-vp-2)
    :parent_space and-sub-frame-2-output))
(define s-and-clause-2-grammar-label
  (def-label :start s-and-clause-2 :parent_concept sentence-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sub-frame-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output))
    :left_branch (StructureCollection s-and)
    :right_branch (StructureCollection s-and-clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) and-sentence-output))
    :left_branch (StructureCollection s-and-clause-1)
    :right_branch (StructureCollection conjunction-super-chunk)))

(def-relation
  :start s-and-subject-1 :end s-and-subject-2 :parent_concept same-concept)
(def-relation
  :start s-and-verb-1 :end s-and-verb-2 :parent_concept same-concept)
(def-relation
  :start s-and-predicate-1 :end s-and-predicate-2 :parent_concept same-concept)

(define conceptual-space-1-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space-1
  (def-conceptual-space :name "" :parent_concept conceptual-space-1-parent-concept
    :no_of_dimensions 1))
(define but-sub-frame-1-input
  (def-contextual-space :name "but-sub-frame-1.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space-1)))
(define but-sub-frame-1-output
  (def-contextual-space :name "but-sub-frame-1.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space-1)))
(define but-sub-frame-1
  (def-frame :name "s-but-sub-1" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space but-sub-frame-1-input
    :output_space but-sub-frame-1-output))
(define but-sub-frame-2-input
  (def-contextual-space :name "but-sub-frame-2.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space-1)))
(define but-sub-frame-2-output
  (def-contextual-space :name "but-sub-frame-2.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space-1)))
(define but-sub-frame-2
  (def-frame :name "s-but-sub-2" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection)
    :input_space but-sub-frame-2-input
    :output_space but-sub-frame-2-output))

(define but-sentence-input
  (def-contextual-space :name "s-but.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space-1)))
(define but-sentence-output
  (def-contextual-space :name "s-but.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space-1)))
(define but-sentence
  (def-frame :name "s-but" :parent_concept sentence-concept :parent_frame None
    :sub_frames (StructureCollection but-sub-frame-1 but-sub-frame-2)
    :concepts (StructureCollection)
    :input_space but-sentence-input
    :output_space but-sentence-output))

(define input-chunk-1
  (def-chunk :locations (list (Location (list (list Nan)) conceptual-space-1)
			       (Location (list) but-sub-frame-1-input)
			       (Location (list) but-sentence-input))
    :parent_space but-sub-frame-1-input))
(define input-chunk-2
  (def-chunk :locations (list (Location (list (list Nan)) conceptual-space-1)
			       (Location (list) but-sub-frame-2-input)
			       (Location (list) but-sentence-input))
    :parent_space but-sub-frame-2-input))
(def-relation :start input-chunk-1 :end input-chunk-2 :parent_concept different-concept
  :locations (list (Location (list) but-sentence-input)
		   (Location (list (list Nan)) same-different-space)
		   (TwoPointLocation (list (list Nan)) (list (list Nan)) conceptual-space-1)))

(define s-but-subject-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :parent_space but-sub-frame-1-output))
(define s-but-subject-1-grammar-label
  (def-label :start s-but-subject-1 :parent_concept nsubj-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-1-output))))
(define s-but-verb-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :parent_space but-sub-frame-1-output))
(define s-but-verb-1-grammar-label
  (def-label :start s-but-verb-1 :parent_concept vb-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-1-output))))
(define s-but-predicate-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :parent_space but-sub-frame-1-output))
(define s-but-predicate-1-grammar-label
  (def-label :start s-but-predicate-1 :parent_concept predicate-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-1-output))))
(define s-but-vp-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :left_branch (StructureCollection s-but-verb-1)
    :right_branch (StructureCollection s-but-predicate-1)
    :parent_space but-sub-frame-1-output))
(define s-but-vp-1-grammar-label
  (def-label :start s-but-vp-1 :parent_concept vp-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-1-output))))
(define s-but-clause-1
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-1-output))
    :left_branch (StructureCollection s-but-subject-1)
    :right_branch (StructureCollection s-but-vp-1)
    :parent_space but-sub-frame-1-output))
(define s-but-clause-1-grammar-label
  (def-label :start s-but-clause-1 :parent_concept sentence-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-1-output))))

(define s-but
  (def-letter-chunk :name "but"
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output))
    :parent_space but-sentence-output
    :abstract_chunk but))

(define s-but-subject-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :parent_space but-sub-frame-2-output))
(define s-but-subject-2-grammar-label
  (def-label :start s-but-subject-2 :parent_concept nsubj-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-2-output))))
(define s-but-verb-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :parent_space but-sub-frame-2-output))
(define s-but-verb-2-grammar-label
  (def-label :start s-but-verb-2 :parent_concept vb-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-2-output))))
(define s-but-predicate-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :parent_space but-sub-frame-2-output))
(define s-but-predicate-2-grammar-label
  (def-label :start s-but-predicate-2 :parent_concept predicate-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-2-output))))
(define s-but-vp-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :left_branch (StructureCollection s-but-verb-2)
    :right_branch (StructureCollection s-but-predicate-2)
    :parent_space but-sub-frame-2-output))
(define s-but-vp-2-grammar-label
  (def-label :start s-but-vp-2 :parent_concept vp-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-2-output))))
(define s-but-clause-2
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output)
		     (Location (list) but-sub-frame-2-output))
    :left_branch (StructureCollection s-but-subject-2)
    :right_branch (StructureCollection s-but-vp-2)
    :parent_space but-sub-frame-2-output))
(define s-but-clause-2-grammar-label
  (def-label :start s-but-clause-2 :parent_concept sentence-concept
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sub-frame-2-output))))

(define conjunction-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output))
    :left_branch (StructureCollection s-but)
    :right_branch (StructureCollection s-but-clause-2)))
(define sentence-super-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list) grammar-space)
		     (Location (list) but-sentence-output))
    :left_branch (StructureCollection s-but-clause-1)
    :right_branch (StructureCollection conjunction-super-chunk)))

(def-relation
  :start s-but-subject-1 :end s-but-subject-2 :parent_concept same-concept)
(def-relation
  :start s-but-verb-1 :end s-but-verb-2 :parent_concept same-concept)
(def-relation
  :start s-but-predicate-1 :end s-but-predicate-2 :parent_concept same-concept)

(define input-space
  (def-contextual-space :name "input" :parent_concept input-concept
    :conceptual_spaces (StructureCollection temperature-space location-space)
    :is_main_input True))

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 0 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 0 4)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 1 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 1 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 1 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 1 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 1 4)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 2 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 4)) temperature-space)
		   (Location (list (list 2 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 2 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 2 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 10)) temperature-space)
		   (Location (list (list 2 4)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 3 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 3 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 3 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 3 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 3 4)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 4 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 4 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 4 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 4 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 4 4)) location-space))
  :parent_space input-space)

(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 5 0)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 5 1)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 16)) temperature-space)
		   (Location (list (list 5 2)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 5 3)) location-space))
  :parent_space input-space)
(def-chunk
  :is_raw True
  :locations (list (Location (list) input-space)
		   (Location (list (list 22)) temperature-space)
		   (Location (list (list 5 4)) location-space))
  :parent_space input-space)

"""


@pytest.fixture(scope="module")
def linguoplotter(program):
    activity_logger = ActivityLogger(sys.stdout)
    loggers = {
        "structure": Mock(),
        "activity": activity_logger,
        "errors": Mock(),
    }
    system = Linguoplotter.setup(loggers=loggers, random_seed=1)
    system.interpreter.interpret_string(program)
    return system
