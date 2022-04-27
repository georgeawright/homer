
(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureCollection temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define magnitude-label-concept
  (def-concept :name "" :is_slot True :parent_space magnitude-space))
(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define ap-sub-frame-input
  (def-contextual-space :name "ap-ap-sub.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection conceptual-space)))
(define ap-sub-frame-output
  (def-contextual-space :name "ap-ap-sub.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space conceptual-space)))
(define ap-sub-frame
  (def-sub-frame  :name "ap-ap-sub" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection)
    :concepts (StructureCollection label-parent-concept)
    :input_space ap-sub-frame-input
    :output_space ap-sub-frame-output))
(define ap-frame-input
  (def-contextual-space :name "ap-frame.meaning" :parent_concept input-concept
    :conceptual_spaces (StructureCollection magnitude-space conceptual-space)))
(define ap-frame-output
  (def-contextual-space :name "ap-frame.text" :parent_concept text-concept
    :conceptual_spaces (StructureCollection grammar-space magnitude-space conceptual-space)))
(define ap-frame
  (def-frame :name "ap[rb,ap]-frame" :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureCollection ap-sub-frame)
    :concepts (StructureCollection magnitude-label-concept)
    :input_space ap-frame-input
    :output_space ap-frame-output))
(define label-start
  (def-link-or-node :locations (list (Location (list (list Nan)) conceptual-space)
				     (Location (list) ap-sub-frame-input)
				     (Location (list) ap-frame-input))
    :parent_space ap-sub-frame-input))
(define label-start-label
  (def-label :start label-start :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list (list Nan)) magnitude-space)
		     (Location (list) ap-sub-frame-input)
		     (Location (list) ap-frame-input))
    :parent_space ap-sub-frame-input))
(define magnitude-label
  (def-label :start label-start-label :parent_concept magnitude-label-concept
    :locations (list (Location (list (list Nan)) magnitude-space)
		     (Location (list (list Nan)) conceptual-space)
		     (Location (list) ap-frame-input))
    :parent_space ap-frame-input))
(define qualifier-word
  (def-letter-chunk :name None
    :locations (list rb-location
		     (Location (list (list Nan)) magnitude-space)
		     (Location (list) ap-frame-output))
    :parent_space ap-frame-output))
(define qualifier-word-grammar-label
  (def-label :start qualifier-word :parent_concept rb-concept
    :locations (list rb-location
		     (Location (list) ap-frame-output))))
(define qualifier-word-magnitude-label
  (def-label :start qualifier-word :parent_concept magnitude-label-concept
    :locations (list (Location (list (list Nan)) magnitude-space)
		     (Location (list (list Nan)) conceptual-space)
		     (Location (list) ap-frame-output))))
(define adjective-word
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output)
		     (Location (list) ap-frame-output))
    :parent_space ap-sub-frame-output))
(define adjective-word-grammar-label
  (def-label :start adjective-word :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) ap-sub-frame-output)
		     (Location (list) ap-frame-output))))
(define adjectival-phrase
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) ap-frame-output))
    :left_branch (StructureCollection qualifier-word)
    :right_branch (StructureCollection adjective-word)
    :parent_space ap-frame-output))
(define adjectival-phrase-grammar-label
  (def-label :start adjectival-phrase :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) ap-frame-output))))

(def-relation :start label-concept :end ap-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start chunk-concept :end ap-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start letter-chunk-concept :end ap-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start jj-concept :end ap-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start rb-concept :end ap-frame
  :is_bidirectional True :activation 1.0)
(def-relation :start ap-concept :end ap-frame
  :is_bidirectional True :activation 1.0)

