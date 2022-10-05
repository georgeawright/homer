(define negativeness-concept
  (def-concept :name "negativeness" :locations (list) :classifier None
    :instance_type Chunk :structure_type Label :parent_space None
    :distance_function centroid_euclidean_distance))
(define negativeness-space
  (def-conceptual-space :name "negativeness" :parent_concept negativeness-concept
    :no_of_dimensions 1 :is_basic_level True))
(define not-concept
  (def-concept :name "not" :locations (list (Location (list (list 0)) negativeness-space))
    :classifier (NotClassifier None) :instance_type Chunk :structure_type Label
    :parent_space negativeness-space :distance_function centroid_euclidean_distance))

(define not-word
  (def-letter-chunk :name "not" :parent_space negativeness-space
    :locations (list (Location (list (list 0)) negativeness-space))))
(def-relation :start not-concept :end not-word :parent_concept jj-concept)
(def-relation :start not-concept :end not-word :parent_concept jjr-concept)
(def-relation :start not-concept :end not-word :parent_concept nn-concept)
(def-relation :start not-concept :end not-word :parent_concept vb-concept)
