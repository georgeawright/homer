(define time-concept
  (def-concept :name "" :is_slot True :parent_space time-space))

(define pp-inessive-time-input
  (def-contextual-space :name "pp[in-time].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection time-space)))
(define pp-inessive-time-output
  (def-contextual-space :name "pp[in-time].text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space time-space)))
(define pp-inessive-time
  (def-frame :name "pp[in-time]"
    :parent_concept pp-inessive-time-concept
    :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection time-concept)
    :input_space pp-inessive-time-input
    :output_space pp-inessive-time-output))

(define chunk
  (def-chunk :locations (list (Location (list (list Nan)) time-space)
			      (Location (list) pp-inessive-time-input))
    :parent_space pp-inessive-time-input))
(define chunk-time-label
  (def-label :start chunk :parent_concept time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-inessive-time-input))
    :parent_space pp-inessive-time-input))

(define pp-word-1
  (def-letter-chunk :name "on"
    :locations (list prep-location
		     (Location (list) pp-inessive-time-output))
    :parent_space pp-inessive-time-output
    :abstract_chunk on))
(define pp-word-2
  (def-letter-chunk :name None
    :locations (list nn-location
		     (Location (list (list Nan)) time-space)
		     (Location (list) pp-inessive-time-output))
    :parent_space pp-inessive-time-output))
(define pp-word-2-grammar-label
  (def-label :start pp-word-2 :parent_concept nn-concept
    :locations (list nn-location
		     (Location (list) pp-inessive-time-output))))
(define pp-word-2-meaning-label
  (def-label :start pp-word-2 :parent_concept time-concept
    :locations (list (Location (list (list Nan)) time-space)
		     (Location (list) pp-inessive-time-output))))

(define pp-super-chunk
  (def-letter-chunk :name None
    :locations (list pp-location
		     (Location (list) pp-inessive-time-output))
    :parent_space pp-inessive-time-output
    :left_branch (StructureCollection pp-word-1)
    :right_branch (StructureCollection pp-word-2)))
(define pp-super-chunk-label
  (def-label :start pp-super-chunk :parent_concept pp-inessive-time-concept
    :locations (list pp-location
		     (Location (list) pp-inessive-time-output))))

(def-relation :start label-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
(def-relation :start pp-concept :end pp-inessive-time
  :is_bidirectional True :activation 1.0)
