(define location-label-concept
  (def-concept :name "" :is_slot True :parent_space location-space))

(define pp-inessive-location-input
  (def-contextual-space :name "pp[in-location].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection location-space)))
(define pp-inessive-location-output
  (def-contextual-space :name "pp[in-location].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space location-space)))
(define pp-inessive-location
  (def-frame :name "pp[in-location]"
    :parent_concept pp-inessive-location-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection location-label-concept)
    :input_space pp-inessive-location-input
    :output_space pp-inessive-location-output))

(define chunk
  (def-chunk :locations (list (Location (list (list Nan Nan)) location-space)
			      (Location (list) pp-inessive-location-input))
    :parent_space pp-inessive-location-input))
(define chunk-location-label
  (def-label :start chunk :parent_concept location-label-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-inessive-location-input))
    :parent_space pp-inessive-location-input))

(define pp-word-1
  (def-letter-chunk :name "in"
    :locations (list prep-location
		     (Location (list) pp-inessive-location-output))
    :parent_space pp-inessive-location-output
    :abstract_chunk in))
(define pp-word-2
  (def-letter-chunk :name "the"
    :locations (list det-location
		     (Location (list) pp-inessive-location-output))
    :parent_space pp-inessive-location-output
    :abstract_chunk the))
(define pp-word-3
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-inessive-location-output))
    :parent_space pp-inessive-location-output))
(define pp-word-3-grammar-label
  (def-label :start pp-word-3 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-inessive-location-output))))
(define pp-word-3-meaning-label
  (def-label :start pp-word-3 :parent_concept location-label-concept
    :locations (list (Location (list (list Nan Nan)) location-space)
		     (Location (list) pp-inessive-location-output))))

(define np-super-chunk
  (def-letter-chunk :name None
    :locations (list np-location
		     (Location (list) pp-inessive-location-output))
    :parent_space pp-inessive-location-output
    :left_branch (StructureCollection pp-word-2)
    :right_branch (StructureCollection pp-word-3)))
(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-inessive-location-output))
    :parent_space pp-inessive-location-output
    :left_branch (StructureCollection pp-word-1)
    :right_branch (StructureCollection np-super-chunk)))
(define pp-super-chunk-label
  (def-label :start pp-super-chunk :parent_concept pp-inessive-location-concept
    :locations (list pp-location
		     (Location (list) pp-inessive-location-output))))

(def-relation :start location-concept :end pp-inessive-location
  :is_bidirectional True :activation 1.0)
